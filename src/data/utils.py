"""Utils for converting prometheus query results to data science friendly formats."""

import sys
import os
import numpy as np
import hashlib
import json
import pandas as pd

from prometheus_api_client import MetricSnapshotDataFrame

# setup logger
import logging

_LOGGER = logging.getLogger(__name__)


def cache_path(cache_dir, key):
    """Determine path to save file to."""
    return os.path.join(cache_dir, key)


def save_to_cache(cache_dir, key, df):
    """Cache query result into a file."""
    if not os.path.exists(cache_dir):
        _LOGGER.warning(
            f"Cache directory {cache_dir} not found. Will attempt to create it"
        )
        os.makedirs(cache_dir)
    df.to_parquet(cache_path(cache_dir, key))


def load_from_cache(cache_dir, key):
    """Load cached query result from a file, if exists."""
    df_path = cache_path(cache_dir, key)
    if os.path.exists(df_path):
        print(f"using cache {key}")
        return pd.read_parquet(df_path)
    else:
        return None


def args_to_cache_key(
    promql,
    metric_type,
    at_timestamp,
    keepcols,
    dropcols,
    numeric_extracol_strategy,
    ts_top1_only,
):
    """Generate unique hash for naming file in which result will be cached."""
    return hashlib.md5(
        json.dumps(
            {
                "promql": promql,
                "metric_type": metric_type,
                "at_timestamp": at_timestamp,
                "keepcols": keepcols,
                "dropcols": dropcols,
                "numeric_extracol_strategy": numeric_extracol_strategy,
                "ts_top1_only": ts_top1_only,
            }
        ).encode()
    ).hexdigest()


def prom_query_to_df_cached(
    prom_conn,
    promql,
    metric_type,
    at_timestamp=None,
    keepcols=None,
    dropcols=None,
    numeric_extracol_strategy="keep",
    ts_top1_only=False,
    cache_dir="data/raw",
):
    """Run prom_query_to_df along with result caching."""
    key = args_to_cache_key(
        promql,
        metric_type,
        at_timestamp,
        keepcols,
        dropcols,
        numeric_extracol_strategy,
        ts_top1_only,
    )
    cached = load_from_cache(cache_dir, key)
    if cached is not None:
        return cached

    df = prom_query_to_df(
        prom_conn,
        promql,
        metric_type,
        at_timestamp,
        keepcols,
        dropcols,
        numeric_extracol_strategy,
        ts_top1_only,
    )
    save_to_cache(cache_dir, key, df)

    return df


def prom_query_to_df(
    prom_conn,
    promql,
    metric_type,
    at_timestamp=None,
    keepcols=None,
    dropcols=None,
    numeric_extracol_strategy="keep",
    ts_top1_only=False,
):
    """Convert an input promql query to a data scientist friendly pandas dataframe.

    Example usage:
    ---------------
    df = prom_query_to_df('cluster_operator_conditions', metric_type='boolean')
    df = prom_query_to_df('cluster_version', metric_type='timestamp')
    df = prom_query_to_df('cluster:memory_usage_bytes:sum', metric_type='numeric')

    Arguments:
        promql {str} -- PromQL query or simply the prometheus metric name
        metric_type {str} -- type of metric. must be one of 'boolean', 'numeric', 'timestamp'
        at_timestamp {int/float} -- value of query at this timestamp is fetched. Defaults to current time.
        keepcols {list} -- list of columns (metric labels) to keep. If not None then dropcols must be None
        dropcols {list} -- list of columns (metric labels) to drop. If not None then keepcols must be None
        numeric_extracol_strategy {str} -- strategy to deal with "extra" columns (labels) in numeric metric types.
                                           Must of one of (keep, drop, onehot)
        ts_top1_only {bool} -- keeps only most recent entry for timestamp metric type

    Returns:
        pd.DataFrame -- dataframe where index is cluster id, columns are features/description-labels
    """
    # name of this funciton, for error messages
    funcname = sys._getframe().f_code.co_name

    # three possible types of telemeter metrics
    allowed_metric_types = ("boolean", "numeric", "timestamp")

    # input sanitization
    metric_type = metric_type.lower()
    assert (
        metric_type in allowed_metric_types
    ), f'Provided metric type "{metric_type}" not recognized. Must be one of {allowed_metric_types}'

    # params for prometheus connect
    pc_params = {}

    # return most recent metrics if time not specified
    if at_timestamp is not None:
        pc_params["time"] = at_timestamp

    # get metric into dataframe
    df = MetricSnapshotDataFrame(prom_conn.custom_query(promql, params=pc_params))

    if df.empty:
        print("EMPTY results from prometheus")
        return df

    df["value"] = df["value"].astype(np.float64)

    # at most one must be specified
    assert (
        keepcols is None or dropcols is None
    ), f"BOTH keepcols and dropcols cannot be specified for function {funcname}"

    # if not specified, try to infer
    if keepcols is None and dropcols is None:
        # columns about telemeter data collection, not directly characteristic of the metric itself
        metacols = [
            "job",
            "endpoint",
            "instance",
            "namespace",
        ]
        # TODO: confirm if these are ok to ignore
        maybe_metacols = [
            "__name__",
            "monitor",
            "prometheus",
            "prometheus_replica",
            "replica",
            "pod",
            "service",
            "block",
            "clustername",
            "k8sCluster",
            "realm",
            "tenant",
        ]
        metacols.extend(maybe_metacols)

        # this metric is instance specific, so 'instance' is useful
        if "instance:" in promql:
            metacols.remove("instance")

        # "useful" columns, characteristic of the metric
        keepcols = df.columns.difference(metacols).tolist()
    elif dropcols is not None:
        # drop the specified columns
        keepcols = df.columns.difference(set(dropcols)).tolist()
    else:
        # keep the specified columns, make sure it is a list (for pandas)
        if not isinstance(keepcols, list):
            _LOGGER.warning(
                f'Input "keepcols" to function {funcname} expected to be type "list" but found type {type(keepcols)}. \
                Will try to cast'
            )
            keepcols = list(keepcols)

    # restructure according to metric type
    if metric_type == "boolean":
        df = _process_boolean_metricdf(df[keepcols])
    elif metric_type == "numeric":
        df = _process_numeric_metricdf(
            df[keepcols], extracol_strategy=numeric_extracol_strategy
        )
    elif metric_type == "timestamp":
        df = _process_timestamp_metricdf(df[keepcols])
    return df


def _process_boolean_metricdf(df):
    # replace empty (nan) entries with the word "empty" so data isnt lost in translation
    pre = df["_id"].nunique()
    df = df.fillna(value="empty")

    # pivot s.t. each row represents a cluster id, and column is MultiIndex of operator name condition,reason
    df = df.pivot_table(
        index="_id", columns=df.columns.drop(["_id", "value"]).tolist(), values="value"
    )
    post = len(df)

    # check if pivoting went ok
    if pre != post:
        _LOGGER.warning(
            f"Some data was lost in translation. Started with {pre} ids, now there are {post} ids"
        )

    # columns descriptive of each cluster id
    _LOGGER.info(f"Each cluster id is described by columns {df.columns.names}")

    # fill nans
    df = df.fillna(0)

    # flatten df (convert multi-dimensional column indexing into single dimnsion)
    if df.columns.nlevels > 1:
        new_colnames = ["_".join(i) for i in df.columns]
    # only one dim. just add colname and then category name
    else:
        new_colnames = [f"{df.columns.names[0]}_{i}" for i in df.columns]
    df.columns = new_colnames
    return df


def _process_numeric_metricdf(df, extracol_strategy="keep"):
    # "unexpected" columns, that are descriptive and not telemeter metadata
    extracols = df.columns.difference(["_id", "value"]).tolist()
    if len(extracols) == 0:
        # no preprocessing needed, return same df but indexed w/ deployment id
        df = df.set_index("_id")
    else:
        _LOGGER.warning(
            f'Other than "value", each cluster id is also characterized by {extracols}'
        )
        _LOGGER.warning(
            "This numeric metric may have multiple values for the same cluster id"
        )

        # keep them as is
        if extracol_strategy == "keep":
            _LOGGER.warning("Returning df with these metrics appended as columns")
            df = df.set_index("_id")
        # drop the extra columns
        elif extracol_strategy == "drop":
            _LOGGER.warning("Dropping extra columns (labels) from metric df")
            df = df.drop(extracols, axis=1).set_index("_id")
        # one hot encode the extra column values
        # FIXME: pivot_table here will have the same issue as in _process_boolean_metricdf
        elif extracol_strategy == "onehot":
            _LOGGER.warning("One hot encoding extra columns")
            # procedure for boolean does pivoting and one hot encoding
            df = _process_boolean_metricdf(df)
    return df


def _process_timestamp_metricdf(df, top1_only=False):
    if df["_id"].duplicated().any() and not top1_only:
        _LOGGER.warning(
            "Found multiple rows for same cluster id, and top1_only is not set to True. \
            So the result df will have multiple rows with the same id and different values"
        )

    # keep only the most recent row
    if top1_only:
        df = df.sort_values(by=["_id", "value"]).drop_duplicates(
            subset="_id", keep="last"
        )

    df = df.set_index("_id")
    return df

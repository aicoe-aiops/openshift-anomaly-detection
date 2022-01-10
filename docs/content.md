# Table of Contents

This project consists of the following main workstreams:

- [Anomaly Detection](#anomaly-detection)
- [Diagnosis Discovery](#diagnosis-discovery)

## Anomaly Detection
In this approach, we try to identify issues before they occur, or before they significantly impact customers. To do so, we find OpenShift deployments that behave "unusually" or "anomalously" as compared to the rest of the fleet. Then, we try to explain this behavior using some heuristics in a way that is actionable for engineers. The outcome of this approach is that each deployment is given an anomaly score, and the explanation for this score is displayed on a Superset dashboard.

* [Notebook](../notebooks/stage/anomaly-detection-demo.ipynb)

## Diagnosis Discovery
In this approach, we first try to determine which deployments exhibit similar types of "symptoms" (i.e. health problems). Once we have this grouping, we try to figure out the precise set of symptoms that best characterizes the underlying issue in each of the groups of deployments. Support engineers can then use these symptom patterns to determine the "diagnosis" for these problematic deployments, and programatically define the issue.

* [Notebook](../notebooks/stage/diagnosis-discovery-demo.ipynb)
* [Blog](../docs/blog/diagnosis-discovery-blog.md)
* [DevConf.CZ 2021 Talk](https://youtu.be/RPBXma8NY0s)

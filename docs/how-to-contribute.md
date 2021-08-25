# Contribute to the OpenShift Anomaly Detection Project

To get started with familiarizing yourself with the project, please check our docs on how to [Get Started](get-started.md).


## Contribute Domain Knowledge

Machine learning models are GIGO - garbage in garbage out. That is, they are only as good as the data they are built on. As data scientists, we rely heavily on storage system SMEs to provide domain knowledge about what pieces of cluster health data can be strong indicators of anomalies, and what patterns in this data can be used to get to meaningful diagnoses. For any feedback you want to provide as an SME, you can open an issue on the project repo[[1]], and prefix the issue title with `SME Feedback:`

## Contribute to ML Analysis

Currently, we have two main machine learning sub-projects/workstreams in this project. To learn more about these ML workstreams, please check out the linked issues or the [content](content.md) docs. Feel free to contribute to any or both of them! Here are some ideas to get you started:

- Anomaly detection
    - Using autoencoders to generate intermediate data representation.
    - Using a probabilistic model (e.g. Local Outlier Probabilities) to generate anomaly scores instead of heuristics.
    - Using statistics other than mean and standard deviation for characterizing etcd behavior.
    - Using model explanation techniques other than LIME and SHAP.
- Diagnosis discovery
    - Using autoencoders to generate intermediate data representation.
    - Using word-based models to generate intermediate data representation.
    - Using TF-IDF instead of hueristics to get most distinguishing symptoms and symptom patterns.

To work on any of these, please leave a comment on the respective issue or create an issue if one doesn't exist. Once you have been assigned to the issue, you can work on it and submit a Pull Request to the project repo[[1]].

## Contribute Data

Currently, this project uses telemetry and insights operator data collected from OpenShift CI clusters. So it is quite possible that this data does not span all possible scenarios and usage patterns in Kubernetes. Therefore, providing operational data from a different set of clusters can be extremely useful for analysis. To do so, please submit a pull request to the project repo[[1]], containing the data, and prefix the PR title with `Data Contribution:`.

## References
* [OpenShift Anomaly Detection GitHub Repo][1]

[1]: https://github.com/aicoe-aiops/openshift-anomaly-detection

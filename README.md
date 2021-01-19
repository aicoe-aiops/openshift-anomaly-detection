# OpenShift Anomaly Detection


### Introduction

A typical OpenShift (or even vanilla kubernetes) cluster consists of several interconnected components working together. So unsurprisingly, there is a variety of ways in which it could break. As a result, it can be time consuming and challenging for engineers to manually inspect and diagnose problematic OpenShift deployments individually, especially at scale. This in turn could hinder smooth customer experience. In this project, we seek to alleviate this issue with the help of machine learning.


### Active Projects

We explore using ML techniques to identify and pre-empt issues that could affect OpenShift deployments. Specifically, we explore the following approaches

#### 1) Anomaly Detection
In this approach, we try to identify issues before they occur, or before they significantly impact customers. To do so, we find deployments that behave anomalously as compared to the rest of the fleet, and then try to explain this behavior. The outcome of this approach is that each deployment is given an anomaly score, and the explanation for this score is displayed on a Superset dashboard.

#### 2) Diagnosis Discovery
In this approach, we first try to determine which deployments exhibit similar types of "symptoms". Then, we try to figure out the precise set of symptoms that best characterizes the underlying problem in those deployments. Support engineers can then use these symptom patterns to determine the "diagnosis" for these problematic deployments, and programatically define the issue.


### Getting Started

We have created a project image and made it accessible through a publicly available JupyterHub instance on the MOC. You can fire up a JupyterHub pod and run our notebooks by following these steps
1. Request access to the MOC cluster according to the steps described [here](https://www.operate-first.cloud/operators/moc-cnv-sandbox/docs/about-the-cluster.md#request-access-to-the-moc-cnv-cluster).
2. Click [here](https://odh-dashboard-opf-dashboard.apps.cnv.massopen.cloud) to get to the ODH dashboard. From there, click the "Launch" button on the panel titled "JupyterHub".

3. Next, click on `Sign in with OpenShift` to continue to authentication. When prompted for an authentication method, choose "MOC-SSO" and then authenticate using your Google or University credentials.
4. In the "Select desired notebook image" dropdown, select `openshift-anomaly-detection:latest` and then click the `Spawn` button.
5. Once your pod is ready and loaded, you should see a directory named `openshift-anomaly-detection-YYYY-MM-DD-HH-mm`. Go to that directory.
6. Finally, go to the `notebooks` directory and click on the notebook(s) you want to run.

**Important Note**: When you're done running the notebooks, please click on the `Control Panel` button on the top right and click `Stop My Server`.

## Contributing

Please feel free to open Issues on this repository, or work on existing Issues and submit Pull Requests.
<br>You may also reach out to our team at [aicoe-aiops@redhat.com](mailto:aicoe-aiops@redhat.com) with any questions.

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

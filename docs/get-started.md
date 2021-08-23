# Get Started

The Jupyter notebooks in this project are intended to be comprehensive, end-to-end notebooks, going through each phase of the machine learning workflow - data understanding and exploration, data cleaning, feature engineering, model training, and model interpretation. So going through these notebooks is a great way to get started with the project.


## Launch Project and Run Notebooks via JupyterHub

To make the notebooks reproducible and executable by everyone, we have containerized and deployed them on the public [JupyterHub](https://jupyterhub-opf-jupyterhub.apps.zero.massopen.cloud) instance on the [Massachusetts Open Cloud](https://massopen.cloud/) (MOC). So you can get access to a Jupyter environment and run our notebooks in just a few clicks! To do so, please follow the steps below:

1. Visit our [JupyterHub](https://jupyterhub-opf-jupyterhub.apps.zero.massopen.cloud), click on `Log in with moc-sso` and sign in using your Google Account.
2. On the spawner page, select `OpenShift Anomaly Detection Notebook Image` for notebook image, `Large - Memory Intensive` for container size, and then click `Start server` to spawn your server.
3. Once your server has spawned, you should see a directory titled `openshift-anomaly-detection-<current-timestamp>`. All the notebooks should be available inside the `notebooks` directory in it for you to explore.

**Note**: When you're done running the notebooks, please go to `File` -> `Hub Control Panel` and click `Stop My Server` to shut down your JupyterHub pod.

## Blog Post and Conference Talk

In addition to exploring the notebooks, you can also read our [blog post](./blog/diagnosis-discovery-blog.md) to get a brief overview of the diagnosis discovery project. Additionally, you can also check out our [conference talk](https://youtu.be/RPBXma8NY0s) at DevConf.CZ 2021 for an in-depth presentation and discussion.

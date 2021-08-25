# OpenShift Anomaly Detection + Diagnosis Discovery
*Applying AI/ML to operational data collected from OpenShift clusters to detect anomalies and diagnose issues*

About 91% of respondents in the CNCF Cloud Native Survey 2020 reported using Kubernetes, 83% of them in production[[1]]. Clearly, Kubernetes is rapidly becoming the defacto standard for container orchestration. Among the available Kubernetes offerings, Red Hat OpenShift was reported to be the leading enterprise Kubernetes platform, built for an open hybrid cloud strategy[[2]].

However, in a typical OpenShift (or other flavors of kubernetes for that matter) deployment there are several interconnected components working together. For example, the apiserver, the etcd, and the scheduler, and so on. So inherently, there is a variety of ways in which such a deployment could break. As a result, it can be time consuming and challenging for engineers to manually inspect and diagnose problematic deployments individually, especially at scale. This in turn could hinder a smooth customer experience.

We believe that these issues can be alleviated with the help of machine learning. To that end, in this project we explore ways to use machine learning to assist in detecting problems early on, as well as to determine the diagnoses for problems. We also open source some operational and health data collected from a set of OpenShift CI clusters, to catalyze community participation in this effort.

* **[Get Started](docs/get-started.md)**

* **[Project Content](docs/content.md)**

* **[How to Contribute](docs/how-to-contribute.md)**

## Contact
This project is maintained by the AIOps teams in the AI Center of Excellence within the Office of the CTO at Red Hat. For more information, reach out to us at aicoe-aiops@redhat.com.

## References
* [CNCF Cloud Native Survery 2020][1]
* [The Forrester Wave™: Multicloud Container Development Platforms Q3 2020 report][2]

[1]: https://www.cncf.io/blog/2020/11/17/cloud-native-survey-2020-containers-in-production-jump-300-from-our-first-survey/
[2]: https://www.redhat.com/en/engage/forrester-wave-multicloud-container-platform-analyst-material

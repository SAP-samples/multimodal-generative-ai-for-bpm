# Multimodal Gen AI
[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/multimodal-generative-ai-for-bpm)](https://api.reuse.software/info/github.com/SAP-samples/multimodal-generative-ai-for-bpm)

## About this project

This repository contains the source code for the thesis `Generative AI for
Business Process Management - Suitability of Modalities`. The goal is evaluate feasibility of creating process models from multimodal documents with generative AI. The repository uses some code and data from the [SAP SAM repository](https://github.com/signavio/sap-sam).



## License

The example code in this repository is licensed as follows. **Note that a different license applies to the dataset itself!**

```
Copyright (c) 2024 by SAP.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

The following license applies to the dataset in the data folder.

```
Copyright (c) 2024 by SAP.

SAP grants to Recipient a non-exclusive copyright license to the Model Collection to use the Model Collection for Non-Commercial Research purposes of evaluating Recipient’s algorithms or other academic research artefacts against the Model Collection. Any rights not explicitly granted herein are reserved to SAP. For the avoidance of doubt, no rights to make derivative works of the Model Collection is granted and the license granted hereunder is for Non-Commercial Research purposes only.

"Model Collection" shall mean all files in the archive (which are JSON, XML, or other representation of business process models or other models).

"Recipient" means any natural person receiving the Model Collection.

"Non-Commercial Research" means research solely for the advancement of knowledge whether by a university or other learning institution and does not include any commercial or other sales objectives.
```

Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/SAP-samples/multimodal-generative-ai-for-bpm).

## Requirements and Setup

We provide two [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) environment.yml files that can be used to create a new environment and install the required dependencies:
- `environment.yml`: contains the abstract dependencies (pandas, numpy, ...).
- `environment-lock.yml`: contains versions for all dependencies and the transitive dependencies to ensure reproducible results.

You can use the following conda command to create the environment:
```shell
conda env create -f environment.yml  
```
or
```shell
conda env create -f environment-lock.yml
``` 


## Getting started

We provide multiple Jupyter Notebooks.

The [data_set_preparation Jupyter Notebook](https://github.com/SAP-samples/multimodal-generative-ai-for-bpm/blob/main/notebooks/00_data_set_preparation.ipynb) provides a walkthrough how the dataset was created.

The [exploring_the_dataset Jupyter Notebook](https://github.com/SAP-samples/multimodal-generative-ai-for-bpm/blob/main/notebooks/01_exploring_the_dataset.ipynb) gives insights about the characteristics of the created dataset.

The [bpmn_generation Jupyter Notebook](https://github.com/SAP-samples/multimodal-generative-ai-for-bpm/blob/main/notebooks/02_bpmn_generation.ipynb) creates process models from multimodal documentations using GPT-4V and zero-shot, one-shot and few-shot prompting.

The [evaluation Jupyter Notebook](https://github.com/SAP-samples/multimodal-generative-ai-for-bpm/blob/main/notebooks/03_evaluation.ipynb) introduces an evaluation framework to calulate similarity scores of the generated process models and the the ground truth models. Furthermore it applies the framework and presents the results.

## Project Organization

    ├── data
    │   ├── examples          <- Some example models for illustrating main ideas.
    |   └── sapsam
    │       ├── cleaned       <- The created dataset.
    |       ├── enriched      <- Original SAP-SAM data set enriched by some meta data
    |       ├── evaluations   <- Evaluation results
    |       ├── generated     <- Generated process models
    |       ├── raw           <- Original SAP-SAM data set
    |       └── tmp           <- Temporary data
    ├── notebooks             <- Jupyter notebooks.
    ├── src               
    |   ├── multimodalgenai   <- Source code for use in this project.
    │   └── sapsam            <- Adapted clone of the [SAP SAM repo](https://github.com/signavio/sap-sam)
    ├── LICENSE               <- License that applies to the example code in this repository.
    ├── README.md             <- The top-level README for developers using this project.
    ├── environment-lock.yml  <- Contains versions for all dependencies and the transitive dependencies to ensure reproducible results.
    ├── environment.yml       <- Contains the abstract dependencies (pandas, numpy, ...).
    └── setup.py              <- Makes project pip installable (pip install -e .) such that src can be imported.

## Support, Feedback, Contributing

This project is open to feature requests/suggestions, bug reports etc. via [GitHub issues](https://github.com/SAP-samples/multimodal-generative-ai-for-bpm/issues). Contribution and feedback are encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](CONTRIBUTING.md).

## Code of Conduct

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone. By participating in this project, you agree to abide by its [Code of Conduct](CODE_OF_CONDUCT.md) at all times.
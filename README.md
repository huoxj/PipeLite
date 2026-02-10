# PipeLite

## What is PipeLite?

PipeLite is a framework that provides modularity and caching support for pipelines, especially data engineering pipeline that contains time-consuming stages.

Each `stage` in the pipeline can be executed independently, with data passed through `artifacts`. 

After excution of a stage, automatic persistence of the output artifacts will be done to avoid redundant computations.

## Features

- Isolate logic into stages that only couple through artifacts
- Persist output artifacts to avoid redundant computations
- Minimal configuration, minimal limitations
- Use decorators and function signatures as conventions so that you can focus on stage logic

## Installation

Currently PipeLite is not published to PyPI. You can install it from source.

## Example

Generate training data and train a model using two stages:

```python
import numpy as np
from pipelite import stage

@stage("gen_data")
class GenerateTrainData:
    def run(self):
        data = np.random.rand(100, 10)
        return { "train_data": data }

@stage("train_model")
class TrainModel:
    def __init__(self, epochs: int):
        self.epochs = epochs
    def run(self, train_data: np.ndarray):
        model = do_train(data=train_data, epochs=self.epochs)
        weights = model.get_weights()
        return { "model_weights": weights }
```

Execute `gen_data`:

```python
from pipelite import Pipeline
Pipeline().run("gen_data")
```

`train_data` artifact will be persisted after `gen_data` stage is executed.

Execute `train_model` in the same way, PipeLite will automatically load the `train_data` and pass it to the `run` method. Finally, `model_weights` will be persisted after `train_model` stage is executed.

## Usage

Todo

## Tricks

Todo

## Todo

- [x] Automatically handle common artifacts
- [ ] Pipeline visualization with mermaid or graphviz
- [ ] Function as a stage
- [ ] Multi-stage execution
- [ ] Stage dependency handling
- [ ] Support phony class as identifier for artifacts

## Why does PipeLite exist?

It is conivenient to use Jupyter notebooks when exploring data and building models. However, when the project grows larger, or when the cell costs too much time to execute, it becomes annoying to organize the code and persist output artifacts to avoid redundant computations. PipeLite is created to manage artifacts automatically and provide modularity for pipeline stages, so that you can focus on your core logic.
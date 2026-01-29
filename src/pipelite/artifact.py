import pickle
import numpy as np
from typing import Any

class Artifact:

    @classmethod
    def load(cls, path: str, **kwargs) -> Any:
        pass

    @classmethod
    def save(cls, obj: Any, path: str, **kwargs):
        pass

class PickleArtifact(Artifact):

    @classmethod
    def load(cls, path: str, **kwargs) -> Any:
        file_path = path + f"/{cls.__name__}.pkl"
        with open(file_path, "rb") as f:
            return pickle.load(f)

    @classmethod
    def save(cls, obj: Any, path: str, **kwargs):
        file_path = path + f"/{cls.__name__}.pkl"
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)

class NumpyArtifact(Artifact):

    @classmethod
    def load(cls, path: str, **kwargs) -> Any:
        file_path = path + f"/{cls.__name__}.npy"
        return np.load(file_path, **kwargs)

    @classmethod
    def save(cls, obj: Any, path: str, **kwargs):
        file_path = path + f"/{cls.__name__}.npy"
        np.save(file_path, obj, **kwargs)
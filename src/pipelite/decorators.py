
from pipelite.artifact import Artifact

# Decorators for stages and artifacts
# Only used for static scanning and interface checking

def stage(
    name: str
):
    def deco(cls: type) -> type:
        # Check if cls has a run() method
        if not hasattr(cls, "run") or not callable(getattr(cls, "run")):
            raise TypeError(f"Class {cls.__name__} must implement a run() method.")
        return cls
    return deco

def artifact(
    name: str
):
    def deco(cls: type[Artifact]) -> type[Artifact]:
        if not issubclass(cls, Artifact):
            raise TypeError(f"Class {cls.__name__} must inherit from Artifact.")
        return cls
    return deco

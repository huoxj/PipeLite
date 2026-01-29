import importlib
import inspect

def parse_class(
    module_name: str,
    cls_name: str
) -> type:
    # Import module
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    if cls is None or not isinstance(cls, type):
        raise ValueError(
            f"Class {cls_name} not found in module {module_name}."
        )
    return cls

def get_method_signatures(cls: type, method: str) -> list[str]:
    if not hasattr(cls, method) or not callable(getattr(cls, method)):
        raise TypeError(f"Class {cls.__name__} doesn't have a {method}() method.")
    
    run_method = getattr(cls, method)
    sig = inspect.signature(run_method)

    sig_names = list(sig.parameters.keys())

    if "self" in sig_names:
        sig_names.remove("self")
    
    return sig_names
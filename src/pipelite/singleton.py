
class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
            instance._inited = False
        return cls._instances[cls]
    
    def __init__(self, *args, **kwargs):
        if not self._inited:
            self._initialize(*args, **kwargs)
            self._inited = True

    def _initialize(self, *args, **kwargs):
        pass
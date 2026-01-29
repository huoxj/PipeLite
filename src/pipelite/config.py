from pydantic import BaseModel

class ConfigModel(BaseModel):
    atf_path: str = "./.tmp"
    scan_depth: int = 3
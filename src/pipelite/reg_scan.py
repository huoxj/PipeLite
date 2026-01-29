import ast
from pathlib import Path

# Static scanner to find and register classes with decorators
# Only register name, module and class info
class RegScanner:
    def __init__(self,
        base_dir: str = ".",
        depth: int = 3,
        dir_exclude: list[str] = ["__pycache__", ".git", ".venv"],
    ):
        self.base = Path(base_dir).resolve()   
        self.depth = depth
        self.dir_exclude = dir_exclude

    def _get_py_files(self) -> list[Path]:
        base = self.base
        blen = len(base.parts)

        py_files = []
        
        stack = [base]
        while stack:
            cur = stack.pop()
            depth = len(cur.parts) - blen

            for item in cur.iterdir():
                if item.is_dir() and item.name not in self.dir_exclude:
                    if depth < self.depth:
                        stack.append(item)
                elif item.is_file() and item.suffix == ".py":
                    py_files.append(item)
        return py_files

    def _parse_pipelite_cls(self,
        file: Path,
        node: ast.ClassDef,
        dec: ast.Call
    ) -> tuple[str, str, str]:
        module_path = file.resolve().relative_to(self.base)
        module_path = ".".join(module_path.with_suffix("").parts)

        class_name = node.name

        stage_name = class_name.lower()
        for i, arg in enumerate(dec.args):
            if i == 0 and isinstance(arg, ast.Constant) \
                and isinstance(arg.value, str):
                stage_name = arg.value
        for kw in dec.keywords:
            if kw.arg == "name" and isinstance(kw.value, ast.Constant) \
                and isinstance(kw.value.value, str):
                stage_name = kw.value.value

        return module_path, class_name, stage_name

    def scan(self) -> tuple[dict, dict]:
        py_files = self._get_py_files()

        stage_to_reg = []
        atf_to_reg = []

        # Collect classes to register
        for pyf in py_files:
            pytree = ast.parse(pyf.read_text())
            for node in ast.walk(pytree):
                if isinstance(node, ast.ClassDef):
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                            if dec.func.id == "stage":
                                stage_to_reg.append((pyf, node, dec))
                            elif dec.func.id == "artifact":
                                atf_to_reg.append((pyf, node, dec))
        
        # Generate registration info
        stages, atfs = {}, {}
        def to_dict(lst, dct):
            for pyf, node, dec in lst:
                mod, cls, name = self._parse_pipelite_cls(pyf, node, dec)
                dct[name] = (mod, cls)
        to_dict(stage_to_reg, stages)
        to_dict(atf_to_reg, atfs)

        return stages, atfs

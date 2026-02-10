import os
import toml

from pipelite.singleton import Singleton
from pipelite.cls_util import parse_class, get_method_signatures
from pipelite.reg_scan import RegScanner
from pipelite.logger import get_logger
from pipelite.config import ConfigModel

class Pipeline(Singleton):
    stages: dict[str, tuple[str, str]]
    stage_params: dict[str, dict]
    artifacts: dict[str, tuple[str, str]]

    def _initialize(self,
        config_path: str = "pipelite.toml",
        stage_params_path: str = "stage_params.toml",
        log_level: str = "INFO"
    ):
        self.logger = get_logger("Pipeline", level=log_level)

        self.config = ConfigModel(**toml.load(config_path))
        self.stage_params = toml.load(stage_params_path)
        self.stages, self.artifacts = RegScanner(
            depth=self.config.scan_depth
        ).scan()
        self.logger.debug(f"Registered stages: {list(self.stages.keys())}")
        self.logger.debug(f"Registered artifacts: {list(self.artifacts.keys())}")

        self.logger.info("Pipeline initialized.")

    def _load_atf(self, name: str):
        # if name not in self.artifacts:
        #     raise ValueError(f"Artifact {name} is not registered.")

        atf_dir = self.config.atf_path + f"/{name}"
        os.makedirs(atf_dir, exist_ok=True)

        # For implicitly declared artifact, use pickle by default
        if name not in self.artifacts:
            from pipelite.artifact import PickleArtifact
            atf = PickleArtifact.load(atf_dir)
        else:
            module_name, cls_name = self.artifacts[name]
            atf_cls = parse_class(module_name, cls_name)
            atf = atf_cls.load(atf_dir)
        return atf
    
    def _save_atf(self, name: str, atf: object):
        atf_dir = self.config.atf_path + f"/{name}"
        os.makedirs(atf_dir, exist_ok=True)

        # For implicitly declared artifact, use pickle by default
        if name not in self.artifacts:
            from pipelite.artifact import PickleArtifact
            PickleArtifact.save(atf, atf_dir)
        else:
            module_name, cls_name = self.artifacts[name]
            atf_cls = parse_class(module_name, cls_name)
            atf_cls.save(atf, atf_dir)

    def run_stage(self,
        name: str
    ):
        if name not in self.stages:
            raise ValueError(f"Stage {name} is not registered.")

        module_name, cls_name = self.stages[name]
        stage_cls = parse_class(module_name, cls_name)

        # Instantiate stage init params
        params = self.stage_params.get(name, {})

        # Instantiate input artifacts
        inputs = get_method_signatures(stage_cls, "run")
        run_inputs = {}
        for atf_name in inputs:
            self.logger.info(
                f"Loading input artifact {atf_name} for stage {name}"
            )
            atf = self._load_atf(atf_name)
            run_inputs[atf_name] = atf

        # Run stage
        self.logger.info(f"Running stage {name}")
        stage = stage_cls(**params)
        outputs = stage.run(**run_inputs)

        # Handle outputs
        outputs = outputs or {}
        for atf_name, atf in outputs.items():
            self.logger.info(
                f"Saving output artifact {atf_name} for stage {name}"
            )
            self._save_atf(atf_name, atf)

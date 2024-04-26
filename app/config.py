from typing import Any

import yaml
from pydantic import BaseModel, Field


class GitProcessorConfig(BaseModel):
    plugin: str
    config: Any = Field(default={})


class Config(BaseModel):
    git_processor: GitProcessorConfig


def read_config() -> Config:
    with open('config.yml') as file:
        return Config.model_validate(yaml.safe_load(file))


config = read_config()

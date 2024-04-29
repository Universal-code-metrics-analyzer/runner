from enum import Enum
from importlib import import_module
from importlib.metadata import entry_points
from typing import Any, Literal, Type

from attrs import define

from core.git_processor import GitProcessor, GitProcessorConfigShape


class PluginType(str, Enum):
    GIT_PROCESSOR = 'git_processor'


@define(frozen=True, kw_only=True)
class Plugin[T]:
    type: PluginType
    module: str
    class_name: str

    def get_class(
        self,
    ) -> Type[T]:
        module = import_module(self.module)
        return getattr(module, self.class_name)


@define(frozen=True, kw_only=True)
class GitProcessorPlugin(Plugin[GitProcessor[GitProcessorConfigShape, Any, Any]]):
    type: Literal[PluginType.GIT_PROCESSOR] = PluginType.GIT_PROCESSOR


class PluginManager:
    _git_processor_plugins: list[GitProcessorPlugin] = []

    def __init__(self):
        for ep in entry_points().select(group='ucma.git_processor.plugin', name='export'):
            module, class_name = ep.value.split(':')
            self._git_processor_plugins.append(
                GitProcessorPlugin(module=module, class_name=class_name)
            )

    def get_git_processor_class(
        self, plugin_name: str
    ) -> type[GitProcessor[GitProcessorConfigShape, Any, Any]]:
        for plugin in self._git_processor_plugins:
            if plugin.module.startswith(plugin_name):
                return plugin.get_class()

        raise Exception(f"Git processor plugin {plugin_name} not found")


plugin_manager = PluginManager()

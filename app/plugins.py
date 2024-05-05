from enum import Enum
from importlib import import_module
from importlib.metadata import entry_points
from typing import Any, Literal, Type, overload

from attrs import define
from core.git_processor import GitProcessor, GitProcessorConfigShape
from core.metrics_calculator import (
    MetricsCalculator,
    MetricsCalculatorConfigShape,
)
from core.report_generator import ReportGenerator, ReportGenratorConfigShape


class PluginType(str, Enum):
    GIT_PROCESSOR = 'git_processor'
    METRICS_CALCULATOR = 'metrics_calculator'
    REPORT_GENERATOR = 'report_generator'


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


@define(frozen=True, kw_only=True)
class MetricsCalculatorPlugin(Plugin[MetricsCalculator[MetricsCalculatorConfigShape]]):
    type: Literal[PluginType.METRICS_CALCULATOR] = PluginType.METRICS_CALCULATOR


@define(frozen=True, kw_only=True)
class ReportGeneratorPlugin(Plugin[ReportGenerator[ReportGenratorConfigShape]]):
    type: Literal[PluginType.REPORT_GENERATOR] = PluginType.REPORT_GENERATOR


class PluginManager:
    _git_processor_plugins: list[GitProcessorPlugin] = []
    _metrics_calculator_plugins: list[MetricsCalculatorPlugin] = []
    _report_generator_plugins: list[ReportGeneratorPlugin] = []

    def discover_plugins[
        T: Plugin[Any]
    ](self, plugin_class: type[T], group: str, name: str = 'export') -> list[T]:
        plugins: list[T] = []
        for ep in entry_points().select(group=group, name=name):
            module, class_name = ep.value.split(':')
            plugins.append(plugin_class(module=module, class_name=class_name))

        return plugins

    def __init__(self):
        self._git_processor_plugins = self.discover_plugins(
            GitProcessorPlugin, group='ucma.git_processor.plugin'
        )

        self._metrics_calculator_plugins = self.discover_plugins(
            MetricsCalculatorPlugin, group='ucma.metrics_calculator.plugin'
        )

        self._report_generator_plugins = self.discover_plugins(
            ReportGeneratorPlugin, group='ucma.report_generator.plugin'
        )

    @overload
    def get_class_from_plugin(
        self, type: Literal[PluginType.GIT_PROCESSOR], plugin_name: str
    ) -> type[GitProcessor[GitProcessorConfigShape, Any, Any]]: ...

    @overload
    def get_class_from_plugin(
        self, type: Literal[PluginType.METRICS_CALCULATOR], plugin_name: str
    ) -> type[MetricsCalculator[MetricsCalculatorConfigShape]]: ...

    @overload
    def get_class_from_plugin(
        self, type: Literal[PluginType.REPORT_GENERATOR], plugin_name: str
    ) -> type[ReportGenerator[ReportGenratorConfigShape]]: ...

    def get_class_from_plugin(self, type: PluginType, plugin_name: str):
        map = {
            PluginType.GIT_PROCESSOR: self._git_processor_plugins,
            PluginType.METRICS_CALCULATOR: self._metrics_calculator_plugins,
            PluginType.REPORT_GENERATOR: self._report_generator_plugins,
        }

        for plugin in map[type]:
            if plugin.module.startswith(plugin_name):
                return plugin.get_class()

        raise Exception(f"Plugin of type '{type}' and name '{plugin_name}' not found")


plugin_manager = PluginManager()

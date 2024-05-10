import asyncio
from typing import Annotated

from typer import Argument, Option, Typer

from app.config import config
from app.plugins import (
    GitProcessorT,
    MetricsCalculatorT,
    PluginType,
    ReportGeneratorT,
    plugin_manager,
)

cli = Typer(no_args_is_help=True)


def get_plugins_classses() -> (
    tuple[type[GitProcessorT], type[MetricsCalculatorT], type[ReportGeneratorT]]
):
    git_processor_class = plugin_manager.get_class_from_plugin(
        PluginType.GIT_PROCESSOR, config.git_processor.plugin
    )
    metrics_calculator_class = plugin_manager.get_class_from_plugin(
        PluginType.METRICS_CALCULATOR, config.metrics_calculator.plugin
    )
    report_generator_class = plugin_manager.get_class_from_plugin(
        PluginType.REPORT_GENERATOR, config.report_generator.plugin
    )

    return (git_processor_class, metrics_calculator_class, report_generator_class)


async def process_ref(
    ref: str,
    git_processor_class: type[GitProcessorT],
    metrics_calculator_class: type[MetricsCalculatorT],
    report_generator_class: type[ReportGeneratorT],
) -> None:

    tree_data = await git_processor_class(config.git_processor.config, ref=ref).process()

    tree_metrics = await metrics_calculator_class(
        config.metrics_calculator.config, tree_data
    ).calculate()

    await report_generator_class(
        config.report_generator.config, tree_metrics=tree_metrics, ref=ref
    ).generate()


async def process_refs(commit_refs: list[str], dry_run: bool) -> None:
    plugin_classess = get_plugins_classses()
    if dry_run:
        return

    tasks = [asyncio.ensure_future(process_ref(ref, *plugin_classess)) for ref in commit_refs]
    await asyncio.gather(*tasks)


@cli.command()
def run(
    commit_refs: Annotated[
        list[str],
        Argument(
            help='List of one of: HEAD, tag, branch name, remote branch name, hash, short hash'
        ),
    ],
    dry_run: Annotated[bool, Option(help='Validate plugin configuration')] = False,
):
    asyncio.run(process_refs(commit_refs, dry_run))

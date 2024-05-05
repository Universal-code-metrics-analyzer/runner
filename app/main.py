import asyncio

from typer import Typer

from app.config import config
from app.plugins import PluginType, plugin_manager

cli = Typer(no_args_is_help=True)


async def process_ref(ref: str) -> None:
    git_processor_class = plugin_manager.get_class_from_plugin(
        PluginType.GIT_PROCESSOR, config.git_processor.plugin
    )
    metrics_calculator_class = plugin_manager.get_class_from_plugin(
        PluginType.METRICS_CALCULATOR, config.metrics_calculator.plugin
    )
    report_generator_class = plugin_manager.get_class_from_plugin(
        PluginType.REPORT_GENERATOR, config.report_generator.plugin
    )

    tree_data = await git_processor_class(config.git_processor.config, ref=ref).process()

    tree_metrics = await metrics_calculator_class(
        config.metrics_calculator.config, tree_data
    ).calculate()

    await report_generator_class(
        config.report_generator.config, tree_metrics=tree_metrics, ref=ref
    ).generate()


async def process_refs(commit_refs: list[str]) -> None:
    tasks = [asyncio.ensure_future(process_ref(ref)) for ref in commit_refs]
    await asyncio.gather(*tasks)


@cli.command()
def main(commit_refs: list[str]):
    asyncio.run(process_refs(commit_refs))


if __name__ == '__main__':
    cli()

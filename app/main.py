import asyncio

from app.config import config
from app.plugins import PluginType, plugin_manager

COMMIT_SHA = 'a89dee02c6fc2fa16bb7e8f8e77fa874a7090632'


async def main():
    git_processor_class = plugin_manager.get_class_from_plugin(
        PluginType.GIT_PROCESSOR, config.git_processor.plugin
    )
    metrics_calculator_class = plugin_manager.get_class_from_plugin(
        PluginType.METRICS_CALCULATOR, config.metrics_calculator.plugin
    )
    report_generator_class = plugin_manager.get_class_from_plugin(
        PluginType.REPORT_GENERATOR, config.report_generator.plugin
    )

    tree_data = await git_processor_class(config.git_processor.config, ref=COMMIT_SHA).process()

    tree_metrics = await metrics_calculator_class(
        config.metrics_calculator.config, tree_data
    ).calculate()

    await report_generator_class(
        config.report_generator.config, tree_metrics=tree_metrics, ref=COMMIT_SHA
    ).generate()


if __name__ == '__main__':
    asyncio.run(main())

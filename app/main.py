import asyncio

from app.config import config
from app.plugins import plugin_manager


async def main():
    git_processor_class = plugin_manager.get_git_processor_class(config.git_processor.plugin)
    metrics_calculator_class = plugin_manager.get_metrics_calculator_class(
        config.metrics_calculator.plugin
    )

    git_processor = git_processor_class(
        config.git_processor.config, commit_sha='1c81a619be55cb2855507eeb2e633e63997ce3e5'
    )

    tree_data = await git_processor.process()
    tree_metrics = await metrics_calculator_class(
        config.metrics_calculator.config, tree_data
    ).calculate()
    print(tree_metrics)


if __name__ == '__main__':
    asyncio.run(main())

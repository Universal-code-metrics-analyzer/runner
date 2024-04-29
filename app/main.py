import asyncio

from app.config import config
from app.plugins import plugin_manager


async def main():
    git_processor_class = plugin_manager.get_git_processor_class(config.git_processor.plugin)
    git_processor = git_processor_class(
        config.git_processor.config, commit_sha='1c81a619be55cb2855507eeb2e633e63997ce3e5'
    )

    print(await git_processor.process())


if __name__ == '__main__':
    asyncio.run(main())

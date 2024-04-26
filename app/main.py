import asyncio

from app.config import config


async def main():
    print(config)


if __name__ == '__main__':
    asyncio.run(main())

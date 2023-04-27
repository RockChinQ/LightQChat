from pkg.utils.config import Config
from pkg.controller import Controller

import logging
import asyncio
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s\t[%(levelname)s]: %(message)s"
)


async def main():
    try:
        _ = Config(
            file_path="config.yaml",
            template_file_path="config-template.yaml"
        )
    except FileNotFoundError as e:
        logging.error(e)
        return

    await Controller().run()
    
    # while True:
    #     time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from yaml import load

from scrapper import Scrapper
from witai import Wixit, Value


async def main():
    with open('settings.yml') as file:
        settings = load(file)
    scrapper = Scrapper()
    war = scrapper.scape('https://en.wikipedia.org/wiki/War')
    charity = scrapper.scape('https://en.wikipedia.org/wiki/Charity_(practice)')
    beer = scrapper.scape('https://en.wikipedia.org/wiki/Beer')
    death = scrapper.scape('https://en.wikipedia.org/wiki/Death')
    witai_settings = settings.get('witai', {})
    witai = Witai(witai_settings.get('entity'), witai_settings.get('token'))
    await wixin.put_words((await war)[0], Value.NEGATIVE)
    await wixin.put_words((await charity)[0], Value.POSITIVE)
    await wixin.put_words((await beer)[0], Value.POSITIVE)
    await wixin.put_words((await death)[0], Value.NEGATIVE)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

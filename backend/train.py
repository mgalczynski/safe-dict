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
    wixin_settings = settings.get('witai', {})
    wixin = Wixit(wixin_settings.get('entity'), wixin_settings.get('token'))
    await wixin.put_words(await war, Value.NEGATIVE)
    await wixin.put_words(await charity, Value.POSITIVE)
    await wixin.put_words(await beer, Value.POSITIVE)
    await wixin.put_words(await death, Value.NEGATIVE)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

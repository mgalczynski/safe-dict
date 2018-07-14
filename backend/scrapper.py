from collections import defaultdict
import re
from socket import gaierror

import html2text
from tornado.httpclient import AsyncHTTPClient, HTTPError


class Scrapper:
    # I think that google bot will receive the most machine readable version of page
    default_user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    # in case of need to handle not latin alphabets change this regex
    regex = re.compile(r'\b(?:[a-zA-Z]+)(?:\'[a-zA-Z]+)?\b')

    # in case of problems with extracting text change settings of html2text or replace with BeautifulSoup or lxml
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    def __init__(self, user_agent=default_user_agent):
        defaults = {
            'user_agent': user_agent
        }
        self.http_client = AsyncHTTPClient(defaults)

    async def scape(self, url):
        if url[:4] != 'http':
            url = 'http://' + url
        try:
            response = await self.http_client.fetch(url)
        except gaierror as e:
            return 400, str(e)
        except ValueError:
            return 400, 'Wrong url, please check if url is correct'

        try:
            text = self.h.handle(response.body.decode('utf-8'))
        except HTTPError:
            # TODO: replace with raise and custom error
            return response.code, response.reason
        except UnicodeDecodeError:
            return 400, 'Response for given url is not a text'

        matches = defaultdict(int)

        for match in self.regex.finditer(text):
            matches[match.group(0).capitalize()] += 1

        return matches, text, response.effective_url

from json import JSONDecodeError
from operator import itemgetter

import tornado.web
from tornado.escape import json_decode

from scrapper import Scrapper


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, repository):
        self.repository = repository

    async def post(self):
        try:
            body = json_decode(self.request.body)
        except JSONDecodeError:
            body = None
        if body is None or not isinstance(body, dict):
            self.set_status(400, 'Body should be JSON dict')
            self.finish()
            return
        url = body.get('url')

        result = await Scrapper().scape(url)

        # in case of errors, will be replaced with custom errors
        if isinstance(result, tuple):
            self.set_status(*result)
            return

        # in case of empty dict
        if not result:
            self.finish({})
            return

        most_frequent = sorted(result.items(), key=itemgetter(1), reverse=True)[:100]

        # we assume that in occurrences is always positive (not zero)
        most_frequent_occurrences = most_frequent[0][1]

        most_frequent = [(w, f / most_frequent_occurrences) for w, f in most_frequent]

        self.finish(dict(most_frequent))
        await self.repository.save(url, result)

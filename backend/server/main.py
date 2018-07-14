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

        most_frequent = sorted(result.items(), key=itemgetter(1), reverse=True)
        most_frequent_occurrences = most_frequent[0][1]
        most_frequent = [{'word': w, 'size': o / most_frequent_occurrences, 'isInTop100': True}
                         for w, o in most_frequent[:100]] + \
                        [{'word': w, 'size': o / most_frequent_occurrences, 'isInTop100': False}
                         for w, o in most_frequent[100:]]

        # we assume that in occurrences is always positive (not zero)

        self.finish({'result': most_frequent})
        await self.repository.save(url, result)

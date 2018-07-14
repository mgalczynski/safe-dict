from base64 import b64encode

import tornado.web


class WordsHandler(tornado.web.RequestHandler):
    def initialize(self, repository):
        self.repository = repository

    async def get(self):
        result = await self.repository.get_all_words()
        # should be replaced with custom exception
        if isinstance(result, tuple):
            self.set_status(*result)
            self.finish()
        else:
            self.finish({'result': [{'word': word.word,
                                     'occurrences': word.occurrences,
                                     'created': str(word.created),
                                     'lastModified': str(word.last_modified)}
                                    for word in sorted(result, key=lambda r: -r.occurrences)]})


class UrlsHandler(tornado.web.RequestHandler):
    def initialize(self, repository):
        self.repository = repository

    async def get(self):
        self.finish({'result': [{
            'url': u.url,
            'hashOfUrl': b64encode(u.hash_of_url).decode(),
            'analysis': u.analysis.name.capitalize(),
            'confidence': u.confidence
        } for u in await self.repository.get_all_urls()]})

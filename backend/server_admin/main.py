import tornado.web


class MainAdminHandler(tornado.web.RequestHandler):
    def initialize(self, repository):
        self.repository = repository

    async def get(self):
        result = await self.repository.get_all_words()
        # should be replaced with custom exception
        if isinstance(result, tuple):
            self.set_status(*result)
            self.finish()
        else:
            self.finish({'result': [{'word': word.word, 'occurrences': word.occurrences} for word in result]})

from enum import Enum, auto
from json import dumps

from tornado.httpclient import AsyncHTTPClient, HTTPClientError


class Value(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()


class Wixit:
    def __init__(self, entity_id, token):
        self.entity_id = entity_id
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.wit.20180714+json'
        }
        self.http_client = AsyncHTTPClient()

    async def put_words(self, words, value):
        value_as_text = value.name.lower()
        body = [{'text': word, 'entities': [{'entity': self.entity_id, 'value': value_as_text}]} for word in words]
        try:
            await self.http_client.fetch('https://api.wit.ai/samples', method='POST', headers=self.headers,
                                         body=dumps(body).encode())
        except HTTPClientError as e:
            raise

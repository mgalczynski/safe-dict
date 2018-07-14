from urllib.parse import quote_plus
from enum import Enum, auto
from json import dumps, JSONDecodeError
from collections import namedtuple

from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient, HTTPClientError
from tornado.escape import json_decode

Analysis = namedtuple('Analysis', ('analysis', 'confidence'))


class Value(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()


class Witai:
    def __init__(self, entity, token):
        self.entity = entity
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.wit.20180714+json'
        }
        self.http_client = AsyncHTTPClient()

    async def put_words(self, words, value):
        value_as_text = value.name.lower()
        body = [{'text': word, 'entities': [{'entity': self.entity, 'value': value_as_text}]} for word in words]
        try:
            await self.http_client.fetch('https://api.wit.ai/samples', method='POST', headers=self.headers,
                                         body=dumps(body).encode())
        except HTTPClientError:
            raise

    async def get_meaning(self, sentence):
        result = await self.http_client.fetch(
            url_concat('https://api.wit.ai/message', {'q': quote_plus(sentence)[:254]}),
            headers=self.headers)
        try:
            body = json_decode(result.body)
        except JSONDecodeError:
            body = {}

        try:
            result = body['entities'][self.entity][0]
            analysis = Analysis(Value[result['value'].upper()], float(result['confidence']))
            if analysis.analysis is None:
                return
            return analysis
        except (KeyError, ValueError):
            pass  # same as return None

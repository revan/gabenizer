"""Module handling records of processing."""

import attr
import datetime
from google.cloud import datastore

import api_module


@attr.s(auto_attribs=True)
class Record:
    source_url: str
    uploaded_url: str
    success: bool
    date: datetime.datetime


_KIND = 'Record'


class Database:

    def __init__(self):
        self._client = None

    @property
    def client(self) -> datastore.Client:
        if not self._client:
            self._client = datastore.Client()
        return self._client

    def contains(self, url: str) -> bool:
        """Checks if we've attempted this url before, successfully or not."""
        return self.get(url) is not None

    def record_post(self, source_url: str, uploaded_url: str) -> Record:
        """Inserts a successful post."""
        r = Record(
            source_url=source_url,
            uploaded_url=uploaded_url,
            success=True,
            date=datetime.datetime.now(),
        )
        self.insert(r)
        return r

    def record_failure(self, url: str) -> Record:
        """Inserts a record to not try this url again."""
        r = Record(
            source_url=url,
            uploaded_url='',
            success=False,
            date=datetime.datetime.now(),
        )
        self.insert(r)
        return r

    @api_module.register
    def insert(self, record: Record):
        task = datastore.Entity(self.client.key(_KIND))
        task.update(attr.asdict(record))
        self.client.put(task)

    def mocked_insert(self, record: Record):
        pass

    @api_module.register
    def get(self, url: str) -> datastore.Entity:
        query = self.client.query(kind=_KIND)
        query.add_filter('source_url', '=', url)
        return next(iter(query.fetch()), None)

    def mocked_get(self, url: str) -> datastore.Entity:
        entity = datastore.Entity()
        for k, v in attr.asdict(Record(
            source_url=url,
            uploaded_url='https://i.imgur.com/ZClFAdK.jpg',
            success=True,
            date=datetime.datetime.now(),
        )).items():
            entity[k] = v
        return entity

'''
import connection

connection = connection.Connection('mysql-connection.json')
config = connection.config
engine = connection.engine
Session = connection.Session
session = connection.Session()
'''


try:
    import simplejson as json
except:
    import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL = ('{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
       '?charset=utf8&use_unicode=1')


class Connection(object):

    def __init__(self, settingfile):
        self._settingfile = settingfile
        self._config = None
        self._engine = None
        self._Session = None

    @property
    def settingfile(self):
        return self._settingfile

    @property
    def config(self):
        if self._config is None:
            with open(self.settingfile) as r:
                self._config = json.load(r)
        return self._config

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                URL.format(**self.config),
                echo=True
            )
        return self._engine

    @property
    def Session(self):
        if self._Session is None:
            self._Session = sessionmaker(self.engine)
        return self._Session

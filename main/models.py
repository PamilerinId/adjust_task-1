from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import DeclarativeMeta

import json
from marshmallow import Schema, fields, post_load


db = SQLAlchemy()

FIELDS = ['date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue']

class Metrics(db.Model):

    __table__name = 'metrics'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(256))
    channel = db.Column(db.String(256))
    country = db.Column(db.String(5))
    os = db.Column(db.String(50))
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    installs = db.Column(db.Integer)
    spend = db.Column(db.Float)
    revenue = db.Column(db.Float)

    @hybrid_property
    def cpi(self):
        return float(self.spend)/int(self.installs)


    def __init__(self,date, channel, country, os, impressions, clicks, installs, spend, revenue, cpi='None'):
        self.date = date
        self.channel = channel
        self.country = country
        self.os = os
        self.impressions = impressions
        self.clicks = clicks
        self.installs = installs
        self.spend = spend
        self.revenue = revenue
        self.cpi = cpi

    def serialise(self):
        return {
        'date': self.date,
        'channel': self.channel,
        'country': self.country,
        'os': self.os,
        'impressions': self.impressions,
        'clicks': self.clicks,
        'installs': self.installs,
        'spend': self.spend,
        'revenue': self.revenue,
        'cpi': self.cpi
        }

    @classmethod
    def find_by_filters(cls, attr):
        search_columns = [getattr(cls, i) for i in attr]
        print(search_columns)
        print(*search_columns)
        return cls.query.with_entities(*search_columns)
    
    @classmethod
    def fetch_columns(cls, attr):
        search_columns = [getattr(cls, i) for i in attr]
        return search_columns


class MetricSchema(Schema):
    date = fields.String(allow_none=True)
    channel = fields.String(allow_none=True)
    country = fields.String(allow_none=True)
    os = fields.String(allow_none=True)
    impressions = fields.String(allow_none=True)
    clicks = fields.Integer(allow_none=True)
    installs = fields.Integer(allow_none=True)
    spend = fields.Float(allow_none=True)
    revenue = fields.Float(allow_none=True)
    cpi = fields.Float(allow_none=True)

    @post_load
    def make_object(self, data):
        return Metrics(**data)




class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
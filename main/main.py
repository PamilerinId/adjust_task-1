import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app, jsonify, make_response
from flask_io import FlaskIO, fields
from sqlalchemy import func, text, desc, asc
from sqlalchemy_utils.functions import sort_query
from .models import db, Metrics, MetricSchema, FIELDS
import json





io = FlaskIO()
metricSchema = MetricSchema(many=True)


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')



@main.route('/metrics', methods=['GET'])
@io.from_query('date_from', fields.String(format="%m-%d-%Y"))
@io.from_query('date_to', fields.String(format="%m-%d-%Y"))
@io.from_query('sort_by', fields.String(missing=''))
@io.from_query('sort_order', fields.String(missing='DESC'))
@io.from_query('group_by', fields.String(missing=''))
@io.from_query('page', fields.Integer(missing=0))
@io.from_query('offset', fields.Integer(missing=0))
@io.from_query('limit', fields.Integer(missing=500))
@io.from_query('cpi', fields.Boolean())
@io.from_query('columns', fields.List(fields.String()))

def fetch_metrics(date_from, date_to, sort_by, sort_order, group_by, page, offset, limit, cpi, columns):

    query = Metrics.query
    fields =FIELDS

    if columns:
        fields = columns[0].split(",")
        model_columns = Metrics.fetch_columns(fields)
        query = query.with_entities(*model_columns)

    if cpi:
        model_columns = Metrics.fetch_columns(fields)
        print((Metrics.spend/Metrics.installs).label("cpi"))
        model_columns.append((Metrics.spend/Metrics.installs).label("cpi"))
        query = query.with_entities(*model_columns)

        if 'cpi' not in fields: #maintain column order
            fields.append('cpi')

    # date filter
    if date_from and date_to:
        query =  query.filter(Metrics.date.between(date_from, date_to))
    elif date_from and not date_to:
        query =  query.filter(Metrics.date >= date_from)
    elif not date_from and date_to:
        query =  query.filter(Metrics.date <= date_to)


    # Group and Sort filter params
    group_by = request.args.to_dict(flat=False)['group_by']
    if sort_by:
        if sort_order == 'ASC': 
            query = query.order_by(asc(text(sort_by)))
        else: 
            query = query.order_by(desc(text(sort_by)))

    if group_by:
        query = query.group_by(*group_by)

    # Pagination Params
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)


    metrics = query.all()

    # oneliner to jsonify
    results =[dict(zip(fields,metric)) for metric in metrics]

    return make_response(jsonify({
    'success':True,
    'results':results,
    'count':len(results)
    }))
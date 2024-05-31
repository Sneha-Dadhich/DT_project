# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy.orm import relationship, sessionmaker, Session
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from datetime import datetime
from sqlalchemy.orm import relationship, create_session
from flask_login import UserMixin, login_required, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract, create_engine, distinct
from flask import request, jsonify
from apps import db, login_manager
from apps.authentication.util import hash_pass
from apps.home import blueprint
from apps.authentication.models import Users


class Search_hist(db.Model, UserMixin):
    __tablename__ = 'search_history'
    search_id       =   db.Column(db.String(64), primary_key=True)
    question        =   db.Column(db.Text)
    answer          =   db.Column(db.Text)
    search_dateTime =   db.Column(db.DateTime(6), default=datetime.now)
    oauth_github    =   db.Column(db.String(100), nullable=True)

def find_user_id_by_username(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        return user.id
    return None

def add_search_to_database(question, answer, oauth_github=None):
    try:
        #user_id=find_user_id_by_username(current_user)
        time=datetime.now()
        search_id =  f"{current_user}_{time.__format__("%y%m%d%H%M%S")}"  # Generating a unique search ID
        search_entry = Search_hist(
            search_id=search_id,
            question=question,
            answer=answer,
            search_dateTime=datetime.now(),
            oauth_github=oauth_github
        )
        db.session.add(search_entry)
        db.session.commit()    
        return 0
    except Exception as e:
        print(e)



def dropdown_data(column, selected_year=0, selected_month=None): 
    session = db.session
    
    year_data = session.query(distinct(extract('year', Search_hist.search_dateTime)).label('year')).order_by('year').all()
    years = [{'year': record.year} for record in year_data]

    if column == "year":
        return years
    
    # If year is selected, extract distinct months for that year
    if selected_year:
        month_data = session.query(distinct(extract('month', Search_hist.search_dateTime)).label('month'))\
                            .filter(extract('year', Search_hist.search_dateTime) == selected_year)\
                            .order_by('month').all()
        months = [{'month': record.month} for record in month_data]
        
        if column == "month":
            return months
        
        # If both year and month are selected, extract distinct days for that year and month
        if selected_month!=None:
            day_data = session.query(distinct(extract('day', Search_hist.search_dateTime)).label('day'))\
                              .filter(extract('year', Search_hist.search_dateTime) == selected_year)\
                              .filter(extract('month', Search_hist.search_dateTime) == selected_month)\
                              .order_by('day').all()
            days = [{'day': record.day} for record in day_data]
        if column=="day":
            return days
        
def search_data(column,year,month,day):
    session = db.session
    print("search data mei pahuch gaye")

    if column=="question":
        print("test case 2 : passed")
        question_searched = session.query(distinct(Search_hist.question).label('question'))\
            .filter(extract('year', Search_hist.search_dateTime) == year)\
            .filter(extract('month', Search_hist.search_dateTime) == month)\
            .filter(extract('day', Search_hist.search_dateTime) == day)\
            .order_by(Search_hist.search_dateTime).all()
        print("test case 3 : passed")
        print(question_searched)
        return jsonify({"question" : {question_searched}})

    if column=="answer":
        print("test case 2 : passed")
        question_searched = session.query(distinct(extract('answer', Search_hist.question)).label('answer'))\
                              .filter(extract('year', Search_hist.search_dateTime) == year)\
                              .filter(extract('month', Search_hist.search_dateTime) == month)\
                              .filter(extract('day', Search_hist.search_dateTime) == day)\
                              .order_by(Search_hist.search_dateTime.time).all()
        print(question_searched)
        return jsonify({"question" : {question_searched}})

'''
        extract('month', Search_hist.search_dateTime).label('month'),
        extract('day', Search_hist.search_dateTime).label('day'),
        extract('hour', Search_hist.search_dateTime).label('hour'),
        extract('minute', Search_hist.search_dateTime).label('minute'),
        extract('second', Search_hist.search_dateTime).label('second')

        'month': record.month,
        'day': record.day,
        'hour': record.hour,
        'minute': record.minute,
        'second': record.second
        
'''

# @blueprint.route('/dashboard.html',methods=["POST"])
# @login_required
# def add_history(question,answer):
#     # if request.method=="POST":
#     #     question=request.form.get()
#     #     answer=request.form.get()
#         add_search_to_database(question,answer,None)
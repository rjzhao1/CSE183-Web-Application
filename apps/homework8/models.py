"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table('notes',
                Field('title', default="New Note"), # Image that is starred
                Field('content', default=""),
                Field('color','integer',default=0),
                Field('author', 'reference auth_user', default=get_user), # User doing the rating.
                Field('starred','boolean',default=False),
                Field('updated', 'datetime', default=get_time,update=get_time),
                )

db.commit()

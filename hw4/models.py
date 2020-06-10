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
     return auth.current_user.get('email')

db.define_table('contact',
         Field('First_Name',requires=IS_NOT_EMPTY()),
         Field('Last_Name',requires=IS_NOT_EMPTY()),
         Field('user_email', default=get_user_email)
         )

db.define_table('phone',
         Field('phone_number',requires=IS_NOT_EMPTY()),
         Field('phone_name',default=""),
         Field('person_id','reference contact',requires=True),
         Field('user_email',default=get_user_email)
         )

db.contact.id.readable = False
db.contact.user_email.readable = False
db.phone.id.readable = False
db.phone.user_email.readable = False

db.commit()

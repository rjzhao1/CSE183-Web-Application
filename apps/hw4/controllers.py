"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
from pydal.validators import *

from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url


url_signer = URLSigner(session)

# The auth.user below forces login.
@action('index', method='GET')
@action.uses('index.html', auth.user,db)
def index():
    user = auth.current_user
    rows=db(db.contact.user_email==auth.current_user.get('email')).select().as_list()
    for row in rows:
        person_id = row["id"]
        phone_numbers = db(db.phone.person_id==person_id).select().as_list()
        formatted_nums = ""
        for phone_number in phone_numbers:
            if formatted_nums!="":
                formatted_nums+=","
            formatted_nums += phone_number["phone_number"]
            formatted_nums += " "
            if phone_number["phone_name"].strip()!="":
                formatted_nums += "(" + phone_number["phone_name"] + ")"
        row["phone_number"] = formatted_nums
    return dict(user=user,rows=rows,url_signer=url_signer)

# The auth.user below forces login.
@action('add_contact',method=['GET', 'POST'])
@action.uses('contact_form.html',session,db)
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

# The auth.user below forces login.
@action('add_contact',method=['GET', 'POST'])
@action.uses('contact_form.html',session,db)
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('edit_contact/<contact_id>', method=['GET', 'POST'])
@action.uses('contact_form.html', session, db)
def edit_contact(contact_id=None):
    # We read the contact.
    c = db.contact[contact_id]
    if c is None or c.user_email!=auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))
    form = Form(db.contact, record=c, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('delete_contact/<contact_id>', method=['GET', 'POST'])
@action.uses(session, db, url_signer.verify())
def delete_contact(contact_id=None):
    # We read the product.
    user = auth.current_user.get('email')
    c = db.contact[contact_id]
    if c is None or c.user_email!=user:
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))
    db(db.contact.id==contact_id).delete()
    redirect(URL('index'))

@action('list_phone/<person_id>', method='GET')
@action.uses('list_phone.html',auth.user,db)
def list_phone(person_id=None):
    name =db.contact[person_id]
    user = auth.current_user.get('email')
    if name is None or name.user_email!=user:
        redirect(URL('index'))
    phone_row=db(db.phone.person_id==person_id).select().as_list()
    return dict(phone_row=phone_row,name=name,url_signer=url_signer)

# The auth.user below forces login.
@action('add_phone/<person_id>',method=['GET', 'POST'])
@action.uses('phone_form.html',session,db)
def add_contact(person_id):
    user = auth.current_user.get('email')
    person = db.contact[person_id]
    if person is None or person.user_email!=user:
        redirect(URL('index'))
    else:
        form = Form([Field('number',requires=IS_NOT_EMPTY()), Field('name')],
                deletable=False,
                csrf_session=session,
                formstyle=FormStyleBulma)
        if form.accepted:
            # We always want POST requests to be redirected as GETs.
            db.phone.insert(
                phone_number=form.vars['number'],phone_name=form.vars['name'],person_id=person_id
            )
            redirect(URL('list_phone',person_id))
    return dict(form=form,user=auth.user)

@action('delete_phone/<person_id>/<phone_id>', method=['GET', 'POST'])
@action.uses(session, db, url_signer.verify())
def delete_contact(person_id=None, phone_id=None):
    # We read the product.
    user = auth.current_user.get('email')
    person = db.contact[person_id]
    if person is None or person.user_email!=user or phone_id is None:
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('list_phone',person_id))
    db(db.phone.id==phone_id).delete()
    redirect(URL('list_phone',person_id))



@action('edit_phone/<person_id>/<phone_id>', method=['GET', 'POST'])
@action.uses('phone_form.html', session, db)
def edit_contact(person_id=None,phone_id=None):
    # We read the contact.
    person = db.contact[person_id]
    user = auth.current_user.get('email')
    phone_number = db.phone[phone_id]

    if (person is None or person.user_email!=user or phone_id is None or
    phone_number is None or phone_number.user_email!=user):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('list_phone',person_id))
    form = Form([Field('number',requires=IS_NOT_EMPTY()), Field('name')],
            deletable=False,
            record = dict(number=phone_number.phone_number,name=phone_number.phone_name),
            csrf_session=session,
            formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        db(db.phone.id == phone_id).update(
            phone_number=form.vars['number'],phone_name=form.vars['name']
        )
        redirect(URL('list_phone',person_id))
    return dict(form=form)

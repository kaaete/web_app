# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, Crud

auth = Auth(db)
service = Service()
plugins = PluginManager()
crud = Crud(db)

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

import urllib

def Hidden(*a,**b):
    b["writable"]=b["readable"]=False
    return Field(*a,**b)


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('item',
    Field('item_name'),
    Field('item_lang', requires=IS_IN_SET([("pt-br", T("Brazilian Portuguese")), ("pt",T("Portuguese")), ("es", T("Spanish")), ("fr", T("French")), ("en-us", T("English (US)"))], zero=T("Select"))),
    Field('item_popular_name'),
    Field('item_short_description', 'text'),
    Field('item_description', 'text'),
    Field('item_use', 'text'),
    Field('item_culinary_use', 'text'),
    Field('item_nutritional_info', 'text'),
    Field('item_image', 'upload'),
    Field('item_slug', compute=lambda row: IS_SLUG()(row.item_name)[0]),
    Field('item_root_id', "integer", default=0),
    auth.signature
    )

db.define_table("item_location",
    Field("item_id", "reference item"),
    Field("address"),
    Field("photo", "upload"),
    Field("location_comment", "text"),
    Field("lat"),
    Field("lng"),
    Field("formatted_address"),
    Field("street_number"),
    Field("postal_code"),
    Field("locality"),
    Field("sublocality"),
    Field("country"),
    Field("country_short"),
    Field("administrative_area_level_1"),
    auth.signature
    )

db.define_table("recipe",
    Field("item_id", "reference item"),
    Field("recipe_title"),
    Field("recipe_content", "text"),
    Field("recipe_image", "upload"),
    Hidden("recipe_likes", "integer"),
    Hidden("recipe_dislikes", "integer"),
    Hidden("recipe_views", "integer"),
    Hidden("recipe_time"),
    Hidden("recipe_difficulty"),
    Hidden("recipe_yield"),
    auth.signature
    )

db.define_table("recipe_item",
    Field("recipe_id", "reference recipe"),
    Field("item_title"),
    auth.signature
    )
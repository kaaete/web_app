# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig

## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])

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

from gluon.tools import Auth, Service, PluginManager, Crud
import urllib

auth = Auth(db)
service = Service()
plugins = PluginManager()
crud = Crud(db)

def Hidden(*a,**b):
    b["writable"]=b["readable"]=False
    return Field(*a,**b)

fields=[
    Field("user_type","string", requires=IS_IN_SET([
                                                    ('0',T("Consumer")),
                                                    ('1',T("Provider")),
                                                    ], zero=T("Select"))),
    Hidden("birthday", "date"),
    Hidden("scholarity"),
    Hidden("school"),
    Hidden("address", "string"),
    Hidden("avatar", "upload"),
    Hidden("lat"),
    Hidden("lng"),
    Hidden("formatted_address"),
    Hidden("street_number"),
    Hidden("postal_code"),
    Hidden("locality"),
    Hidden("sublocality"),
    Hidden("country"),
    Hidden("country_short"),
    Hidden("administrative_area_level_1"),
    Hidden("profile_complete", "boolean", default=False)
    ]

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
auth.settings.everybody_group_id = 'user'
auth.settings.create_user_groups = False
auth.settings.register_next = URL('default', 'index')
auth.settings.extra_fields["auth_user"] = fields
auth.settings.login_after_registration = True

auth.settings.profile_next = URL(c='garden', f='index')
auth.settings.change_password_next = URL(c='garden', f='index')
auth.settings.reset_password_next = URL(c='garden', f='index')
auth.settings.retrieve_password_next = URL(c='garden', f='index')

auth.messages.email_sent = 'Verifique seu email para confirmar a solicitação.'
auth.messages.reset_password = T('Clique no link http://')+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+T('/%(key)s para recuperar sua senha')
auth.messages.password_changed = 'Senha alterada com sucesso.'

auth.settings.change_password_next = URL(c='default', f='index')
auth.settings.reset_password_next = URL(c='default', f='index')
auth.settings.verify_email_next = URL(c='default', f='index')
auth.settings.retrieve_password_next = URL(c='default', f='index')
auth.settings.request_reset_password_next = URL(c='default', f='index')
auth.messages.logged_in = T("Welcome to Ka'a-eté!")
auth.messages.logged_out = T("See you later!")

auth.define_tables(username=True, signature=False)
auth.settings.login_userfield = 'email'
crud.settings.formstyle = 'divs'

db.auth_user.last_name.readable = db.auth_user.last_name.writable = False
db.auth_user.username.readable = db.auth_user.username.writable = False
db.auth_user.avatar.readable = db.auth_user.avatar.writable = False
db.auth_user.address.readable = db.auth_user.address.writable = False


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
    Field('item_slug', compute=lambda row: IS_SLUG()(row.item_popular_name.split(",")[0])[0]),
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
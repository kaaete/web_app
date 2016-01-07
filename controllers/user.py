# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    redirect(URL(c='default', f='index'))

def register():
    form = auth.register()
    return locals()

@auth.requires_login()
def profile():
    form = auth.profile()
    return locals()

@auth.requires_login()
def change_password():
    form = auth.change_password(next=URL(c='garden', f='index'))
    return locals()

def new_password():
    form = auth()
    form.element(_name='new_password')['_autofocus'] = "autofocus"
    form.element(_name='new_password')['_class'] = "form-control"
    form.element(_name='new_password2')['_class'] = "form-control"

    return locals()

@auth.requires_login()
def delete_account():
	import time
	import hashlib

	deleted_email = str(time.time())+"@deleted_email.com"
	deleted_pass = hashlib.sha224(str(time.time())).hexdigest()
	deleted_user = str(time.time())
	deleted_name = str(time.time())

	update_user = db(db.auth_user.id == auth.user.id).update(
		first_name = deleted_name,
		last_name = deleted_name,
		email = deleted_email,
		password = deleted_pass,
		profile_complete = False,
		user_type = 2
		)

	session.flash = T("Account deleted successfully!")
	redirect(URL(c='default', f='user', args="logout"))   
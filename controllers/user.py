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
    
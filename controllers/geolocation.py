# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def get_item_location():
    item_id = request.vars.item or redirect(URL(c='default', f='index'))
    itens = db((db.item.id == item_id)&(db.item_location.item_id == item_id)).select()

    return dict(itens=itens)

def get_itens_location():
    itens = db((db.item.id > 0)&(db.item_location.item_id == db.item.id)).select()

    return dict(itens=itens)
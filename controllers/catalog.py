# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def detail():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()

    return locals()

def item_add_location_list():
    itens = db(db.item.id > 0).select(orderby=db.item.item_name)

    return locals()

def add_location():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()
    form = crud.create(db.item_location,
        message = T("Item location added with success."),
        next = URL(c='catalog', f='detail', args=item_id)
        )

    return locals()


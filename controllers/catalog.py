# -*- coding: utf-8 -*-

def detail():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()

    return locals()

def item_add_location_list():
    itens = db(db.item.id > 0).select(orderby=db.item.item_name)

    return locals()

@auth.requires_login()
def add_location():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item_slug = request.args(1)
    item = db(db.item.id == item_id).select()
    form = crud.create(db.item_location,
        message = T("Item location added with success."),
        next = URL(c='catalog', f='detail', args=[item_id, item_slug])
        )

    return locals()


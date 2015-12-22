# -*- coding: utf-8 -*-

def get_item_location():
    item_id = request.vars.item or redirect(URL(c='default', f='index'))
    itens = db((db.item.id == item_id)&(db.item_location.item_id == item_id)).select()

    return dict(itens=itens)

def get_itens_location():
    itens = db((db.item.id > 0)&(db.item_location.item_id == db.item.id)).select()

    return dict(itens=itens)
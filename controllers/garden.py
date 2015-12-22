# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    itens = db(db.item.created_by == auth.user.id).select()
    recipies = db(db.recipe.created_by == auth.user.id).select()
    points = db((db.item_location.created_by == auth.user.id)&(db.item.id == db.item_location.item_id)).select()

    return locals()

def edit_item():
    item_id = request.args(0) or redirect(URL(c='garden', f='index'))
    form = crud.update(db.item, item_id, next=URL(c='garden', f='index'))
    return locals()

def add_item():
    form = crud.create(db.item, next=URL(c='garden', f='index'))
    return locals()

def detail():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()

    return locals()

def add_recipe():
    form = crud.create(db.recipe, next=URL(c='garden', f='index'), messages=T("Recipie add successfully"))
    return locals()

def add_recipe_list():
    itens = db(db.item.id > 0).select(orderby=db.item.item_name)

    return locals()
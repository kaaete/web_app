# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    itens = db(db.item.created_by == auth.user.id).select()
    recipies = db(db.recipe.created_by == auth.user.id).select()
    points = db((db.item_location.created_by == auth.user.id)&(db.item.id == db.item_location.item_id)).select()

    return locals()

@auth.requires_membership("admin")
def edit_item():
    item_id = request.args(0) or redirect(URL(c='garden', f='index'))
    form = crud.update(db.item, item_id, next=URL(c='garden', f='index'))
    return locals()

@auth.requires_membership("admin")
def add_item():
    form = crud.create(db.item, next=URL(c='garden', f='index'))
    return locals()

def detail():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()

    return locals()

@auth.requires_membership("admin")
def add_recipe():
    form = crud.create(db.recipe, next=URL(c='garden', f='index'), messages=T("Recipie add successfully"))
    return locals()

def add_recipe_list():
    itens = db(db.item.id > 0).select(orderby=db.item.item_name)

    return locals()

@auth.requires_login()
def edit_location():
    location_id = request.args(0) or redirect(UR(c='garden', f='index'))

    location = db((db.item_location.id == location_id)&(db.item.id == db.item_location.item_id)).select(
        db.item.item_popular_name,
        db.item.id,
        db.item_location.ALL
        )

    for l in location: 
      item_id = l.item.id
      comment = l.item_location.location_comment
      plant = l.item.item_popular_name
      point_address = l.item_location.formatted_address
      response.address = l.item_location.formatted_address

    #restore the original value of the field "id" changed by the geocomplete lib
    #before call crud update
    request.post_vars.id = location_id

    form = crud.update(db.item_location,
        location_id,
        message = T("Item location edited with success."),
        next = URL(c='garden', f='index')
        )
    return locals()

@auth.requires_login()
def delete_location():
    item_id = request.args(0) or redirect(UR(c='garden', f='index'))
    delete_item = db((db.item_location.id == item_id)&(db.item_location.created_by == auth.user.id)).delete()
    if not delete_item:
        session.flash = T("You don't have permission to delete it.")
    else:
        session.flash = T("Item deleted.")

    redirect(URL(c='garden', f='index'))
# -*- coding: utf-8 -*-

def detail():
    item_id = request.args(0) or redirect(UR(c='default', f='index'))
    item = db(db.item.id == item_id).select()

    return locals()

def item_add_location_list():
    itens = db(db.item.id > 0).select(orderby=db.item.item_name)

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


@auth.requires_login()
def edit_location():
    item_id = request.args(0) or redirect(UR(c='garden', f='index'))
    location_id = request.args(1)
    item = db(db.item.id == item_id).select()
    locations = db(db.item_location.id == location_id).select()

    for l in locations:
        address = l.formatted_address

    response.address = address

    form = crud.update(db.item_location,
        location_id,
        message = T("Item location edited with success."),
        next = URL(c='garden', f='index')
        )

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


# -*- coding: utf-8 -*-

def index():
    itens = db(db.item.id > 0).select(orderby='item_popular_name')
    return locals()

def team():
    return locals()

def about():
    return locals()

def contact():
    send = False
    if request.post_vars:
        send = True
        name = request.post_vars.name
        email = request.post_vars.email
        message = request.post_vars.message

        subject = T("Contact received")
        content = """<html>
            <strong>"""+T("Name")+""":</strong>"""+name+"""<br>
            <strong>"""+T("Email")+""":</strong>"""+email+"""<br>
            <strong>"""+T("Message")+""":</strong>"""+str(message)+"""<br>
        </html>"""

        send_mail = mail.send(myconf.take('smtp.sender'),
            subject,
            content,
            reply_to = email
            )
        
        if not send_mail:
            success = False
        else:
            success = True

    return locals()

def nus():
    return locals()

def error():
    return locals()

def logout():
    auth.logout(next=URL(c='default', f='index'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



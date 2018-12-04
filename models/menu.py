# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(IMG(_src=URL('static', 'images/icon.png'),_href=URL('default', 'index')))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Laboratorio de Química Teórica - LQT - lavecchia.at.gmail.com'
response.meta.description = 'NaturAr: base de datos de compuestos naturales de la Argentina'
response.meta.keywords = 'compuestos naturales, base de datos, estructura molecular, moléculas'
response.meta.generator = 'NaturAr'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    #~ (T('Research Groups'), False, URL('groups', 'list'), []),
    (T('Compounds'), False, URL('compuestos', 'buscar'), []),
    (T('+Info'), False, None, [
		#~ (T('Changelog'), False, URL('info', 'changelog'), []),
        (T('ToDo list'), False, URL('info', 'todo'), []),
		(T('About NaturAr'), False, URL('info', 'about'), []),
    ]),
    #~ (T('Extracts'), False, URL('extracts', 'buscar'), [])
	]

if auth.is_logged_in():
    response.menu.extend(
        [(T('Submission'), False, None, 
        [
            (T('Compound'), False, URL('submission', 'submit_compound'),[]),
            (T('Submitted Compound'), False, URL('submission', 'compound_submitted'),[]),
        
        ])]
        )
    #~ response.menu.extend(
        #~ [(T('Messaging'), False, URL('messaging', 'inbox'), [])]
        #~ )
    response.menu.extend(
        [(T('Dowload'), False, None, 
        [
            (T('All Structures'), False, URL('compuestos', 'get_allmol'),[]),
            (T('All except semisynthetic'), False, URL('compuestos', 'get_allnatural'),[]),
        
        ])]
        )


DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
          (T('This App'), False, '#', [
              (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
              LI(_class="divider"),
              (T('Controller'), False,
               URL(
               'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
              (T('View'), False,
               URL(
               'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
              (T('DB Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/db.py' % app)),
              (T('Menu Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/menu.py' % app)),
              (T('Config.ini'), False,
               URL(
               'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
              (T('Layout'), False,
               URL(
               'admin', 'default', 'edit/%s/views/layout.html' % app)),
              (T('Stylesheet'), False,
               URL(
               'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
              (T('Database'), False, URL(app, 'appadmin', 'index')),
              (T('Errors'), False, URL(
               'admin', 'default', 'errors/' + app)),
              (T('About'), False, URL(
               'admin', 'default', 'about/' + app)),
              ]),
          
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 


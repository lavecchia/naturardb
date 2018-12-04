

def todo():
   return dict(message=T('TODO List'))

def about():
   return dict(message=T('About'))

@cache.action(time_expire=300, cache_model=cache.ram, quick='P')
def changelog():
    import os
    filename = os.path.join(request.env.gluon_parent, 'CHANGELOG')
    return response.render(dict(changelog=MARKMIN(read_file(filename))))

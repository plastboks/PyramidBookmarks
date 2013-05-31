from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import remember, forget
from pyramid.security import authenticated_userid

from sqlalchemy.exc import DBAPIError

from pyramid.view import (
  view_config,
  forbidden_view_config,
  )

from .models import (
  DBSession,
  User,
  Bookmark,
  )

from .forms import (
  BookmarkCreateForm,
  BookmarkUpdateForm,
  UserRegisterForm,
  UserProfileForm,
  )


#################
# Bookmark CRUD #
#################
@view_config(route_name='index', 
             renderer='pyramarks:templates/index.mako',
             permission='view')
def index_page(request):
  page = int(request.params.get('page', 1))
  user = User.by_id(authenticated_userid(request))
  paginator = user.bookmarks(page)
  return {'paginator':paginator, 
          'username':user.username,
          'title':'Home'}

@view_config(route_name='bookmark_action', 
             renderer='pyramarks:templates/edit_bookmark.mako',
             match_param='action=create',
             permission='create')
def bookmark_create(request):
  bookmark = Bookmark()
  form = BookmarkCreateForm(request.POST)
  if request.method == 'POST' and form.validate():
    form.populate_obj(bookmark)
    user_id = authenticated_userid(request)
    bookmark.owner_id = user_id
    DBSession.add(bookmark)
    request.session.flash('Bookmark %s created' % (bookmark.title))
    return HTTPFound(location=request.route_url('index'))
  return {'form':form, 
          'action':request.matchdict.get('action'),
          'title':'New'}

@view_config(route_name='bookmark_action',
             renderer='pyramarks:templates/edit_bookmark.mako',
             match_param='action=edit',
             permission='edit')
def bookmark_edit(request):
  user = User.by_id(authenticated_userid(request))
  id = int(request.params.get('id', -1))
  bookmark = user.bookmark(id)
  if not bookmark:
    return HTTPNotFound()
  form = BookmarkUpdateForm(request.POST, bookmark)
  if request.method == 'POST' and form.validate():
    form.populate_obj(bookmark)
    return HTTPFound(location=request.route_url('bookmark',
                                                id=bookmark.id,
                                                slug=bookmark.slug))
  return {'form':form, 
          'action':request.matchdict.get('action'),
          'title':'Edit'+bookmark.title}

@view_config(route_name='bookmark_action',
             renderer='string',
             match_param='action=delete',
             permission='delete')
def bookmark_delete(request):
  user = User.by_id(authenticated_userid(request))
  id = int(request.params.get('id', -1))
  bookmark = user.bookmark(id)
  if bookmark:
    DBSession.delete(bookmark)
    return HTTPFound(location=request.route_url('index'))
  return HTTPNotFound()


################
# User section #
################
@view_config(route_name='register',
             renderer='pyramarks:templates/register.mako')
def user_register(request):
  form = UserRegisterForm(request.POST)
  user = User()
  if request.method == "POST" and form.validate():
    form.populate_obj(user)  
    user.password = user.hash_password(form.password.data)
    DBSession.add(user)
    request.session.flash('User registered')
    return HTTPFound(location=request.route_url('login'))
  return {'form':form,
          'action':request.matchdict.get('action'),
          'title':'Register'}

@view_config(route_name='profile',
             renderer='pyramarks:templates/profile.mako',
             permission='view')
def user_profile(request):
  user = User.by_id(authenticated_userid(request))
  form = UserProfileForm(request.POST, user)
  if request.method == 'POST' and form.validate():
    form.populate_obj(user)
    if form.password.data:
      user.password = user.hash_password(form.password.data)
    else:
      del user.password
    DBSession.add(user)
    request.session.flash('User %s updated' % (user.username))
    return HTTPFound(location=request.route_url('index'))
  return {'form':form,
          'action':request.matchdict.get('action'),
          'title':'Profile'}


########################
# Login/logout section #
########################
@view_config(route_name='login',
             renderer='pyramarks:templates/login.mako')
@view_config(route_name='login',
             renderer='string',
             request_method='POST')
@forbidden_view_config(renderer='pyramarks:templates/login.mako')
def bookmark_login(request):
  if request.method == "POST" and request.POST.get('username'):
    user = User.by_uname_email(request.POST.get('username'))
    if user and user.verify_password(request.POST.get('password')):
      headers = remember(request, user.id)
      return HTTPFound(location=request.route_url('index'),
                       headers=headers)
    headers = forget(request)
    request.session.flash('Login failed')
    return HTTPFound(location=request.route_url('login'),
                     headers=headers)
  if authenticated_userid(request):
    return HTTPFound(location=request.route_url('index'))
  return {'action':request.matchdict.get('action'),
          'title':'Login'}

@view_config(route_name='logout',
             renderer='string')
def bookmark_logout(request):
  headers = forget(request)
  return HTTPFound(location=request.route_url('login'),
                   headers=headers)


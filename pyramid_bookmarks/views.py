from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
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
  )


@view_config(route_name='index', 
             renderer='pyramid_bookmarks:templates/index.mako',
             permission='view')
@forbidden_view_config(renderer='pyramid_bookmarks:templates/login.mako')
def index_page(request):
  page = int(request.params.get('page', 1))
  paginator = Bookmark.get_paginator(request, page)
  user = User.by_id(authenticated_userid(request))
  if user:
    return {'paginator':paginator, 'username':user.username}
  return HTTPFound(location=request.route_url('login'))

@view_config(route_name='bookmark', 
             renderer='pyramid_bookmarks:templates/view_bookmark.mako',
             permission='view')
def bookmark_view(request):
  id = int(request.matchdict.get('id', -1))
  bookmark = Bookmark.by_id(id)
  if not bookmark:
    return HTTPNotFound()
  return {'bookmark':bookmark}  


@view_config(route_name='bookmark_action', 
             renderer='pyramid_bookmarks:templates/edit_bookmark.mako',
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
    return HTTPFound(location=request.route_url('index'))
  return {'form':form, 
          'action':request.matchdict.get('action')}


@view_config(route_name='bookmark_action',
             renderer='pyramid_bookmarks:templates/edit_bookmark.mako',
             match_param='action=edit',
             permission='edit')
def bookmark_edit(request):
  id = int(request.params.get('id', -1))
  bookmark = Bookmark.by_id(id)
  if not bookmark:
    return HTTPNotFound()
  form = BookmarkUpdateForm(request.POST, bookmark)
  if request.method == 'POST' and form.validate():
    form.populate_obj(bookmark)
    return HTTPFound(location=request.route_url('bookmark',
                                        id=bookmark.id,
                                        slug=bookmark.slug))
  return {'form':form, 'action':request.matchdict.get('action')}


@view_config(route_name='bookmark_action',
             renderer='string',
             match_param='action=delete',
             permission='delete')
def bookmark_delete(request):
  id = int(request.params.get('id', -1))
  bookmark = Bookmark.by_id(id)
  if not bookmark:
    return HTTPNotFound()
  DBSession.delete(bookmark)
  return HTTPFound(location=request.route_url('index'))


@view_config(route_name='login',
             renderer='pyramid_bookmarks:templates/login.mako')
@view_config(route_name='login',
             renderer='string',
             request_method='POST')
def bookmark_login(request):
  if request.method == "POST" and request.POST.get('username'):
    user = User.by_username(request.POST.get('username'))
    if user and user.verify_password(request.POST.get('password')):
      headers = remember(request, user.id)
      return HTTPFound(location=request.route_url('index'),
                       headers=headers)
    else:
      headers = forget(request)
      return HTTPFound(location=request.route_url('login'),
                     headers=headers)
  else:
    return {'action':request.matchdict.get('action')}


@view_config(route_name='logout',
             renderer='string')
def bookmark_logout(request):
  headers = forget(request)
  return HTTPFound(location=request.route_url('login'),
                   headers=headers)

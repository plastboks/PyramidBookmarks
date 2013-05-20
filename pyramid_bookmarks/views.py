from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
  DBSession,
  User,
  Bookmark,
  )

from .forms import (
  BookmarkCreateForm,
  BookmarkUpdateForm,
  )


@view_config(route_name='home', 
             renderer='pyramid_bookmarks:templates/index.mako')
def index_page(request):
  page = int(request.params.get('page', 1))
  paginator = Bookmark.get_paginator(request, page)
  return {'paginator':paginator}

@view_config(route_name='bookmark', 
             renderer='pyramid_bookmarks:templates/view_bookmark.mako')
def bookmark_view(request):
  id = int(request.matchdict.get('id', -1))
  bookmark = Bookmark.by_id(id)
  if not bookmark:
    return HTTPNotFound()
  return {'bookmark':bookmark}  


@view_config(route_name='bookmark_action', 
             renderer='pyramid_bookmarks:templates/edit_bookmark.mako',
             match_param='action=create')
def bookmark_create(request):
  bookmark = Bookmark()
  form = BookmarkCreateForm(request.POST)
  if request.method == 'POST' and form.validate():
    form.populate_obj(bookmark)
    DBSession.add(bookmark)
    return HTTPFound(location=request.route_url('home'))
  return {'form':form, 'action':request.matchdict.get('action')}


@view_config(route_name='bookmark_action',
             renderer='pyramid_bookmarks:templates/edit_bookmark.mako',
             match_param='action=edit')
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


@view_config(route_name='auth',
             match_param='action=in',
             renderer='string',
             request_method='POST')
@view_config(route_name='auth',
             match_param='action=out',
             renderer='string')
def sign_in_out(request):
  return {}

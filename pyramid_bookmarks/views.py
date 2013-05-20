from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    Bookmark,
    )


@view_config(route_name='home', 
             renderer='pyramid_bookmarks:templates/index.mako')
def index_page(request):
  page = int(request.params.get('page', 1))
  paginator = Bookmark.get_paginator(request, page)
  return {'paginator':paginator}

@view_config(route_name='bookmark', 
             renderer='pyramid_bookmarks:templats/view_bookmark.mako')
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
  return {}


@view_config(route_name='bookmark_action',
             renderer='pyramid_bookmarks:templates/edit_bookmarks.mako',
             match_param='action=edit')
def bookmark_edit(request):
  return {}


@view_config(route_name='auth',
             match_param='action=in',
             renderer='string',
             request_method='POST')
@view_config(route_name='auth',
             match_param='action=out',
             renderer='string')
def sign_in_out(request):
  return {}

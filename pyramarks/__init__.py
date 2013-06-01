from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .security import (
  EntryFactory,
  )

from .models import (
  DBSession,
  Base,
  )


def main(global_config, **settings):
  """ This function returns a Pyramid WSGI application.
  """
  engine = engine_from_config(settings, 'sqlalchemy.')
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  authenPol = AuthTktAuthenticationPolicy('verysecret')
  authorPol = ACLAuthorizationPolicy()
  sess_factory = UnencryptedCookieSessionFactoryConfig('itisverysecret')
  config = Configurator(settings=settings,
                        authentication_policy = authenPol,
                        authorization_policy = authorPol,
                        root_factory='pyramarks.security.EntryFactory',
                        session_factory=sess_factory
                        )
  config.add_static_view('static', 'static', cache_max_age=3600)
  config.add_route('index', '/')
  config.add_route('new', '/new')
  config.add_route('edit', '/edit')
  config.add_route('delete', '/delete')
  config.add_route('search_tag', '/search/tag')
  config.add_route('search', '/search')
  config.add_route('register', '/register')
  config.add_route('profile', '/profile')
  config.add_route('login', '/login')
  config.add_route('logout', '/logout')
  config.scan()
  return config.make_wsgi_app()

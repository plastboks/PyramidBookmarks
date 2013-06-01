import os
import sys
import transaction
import getpass

from cryptacular.bcrypt import BCRYPTPasswordManager

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    User,
    Bookmark,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    manager = BCRYPTPasswordManager()
    pw = getpass.getpass('Admin password: ')
    hashed = manager.encode(pw)
    
    with transaction.manager:
        admin = User(username=u'admin', email='admin@admin.local', password=hashed)
        DBSession.add(admin)

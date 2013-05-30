from wtforms import (
  Form,
  BooleanField,
  TextField,
  TextAreaField,
  validators,
  HiddenField,
  PasswordField, 
  )

strip_filter = lambda x: x.strip() if x else None

class BookmarkCreateForm(Form):
  title = TextField('Bookmark title',
                    [validators.Length(min=1, max=255)],
                    filters=[strip_filter])
  url = TextField('Bookmark URL',
                      [validators.Length(min=1, max=512),
                       validators.URL(require_tld=False,
                                      message='Not a valid URL')],
                      filters=[strip_filter])

class BookmarkUpdateForm(BookmarkCreateForm):
  id = HiddenField()


class UserRegisterForm(Form):
    username = TextField('username',
                         [validators.Length(min=4, max=32)],
                         filters=[strip_filter])
    email = TextField('email',
                      [validators.Length(min=4, max=320),
                       validators.Email(message='Not a valid email address')],
                      filters=[strip_filter])
    password = PasswordField('password',
                             [validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must match')],
                             filters=[strip_filter])
    confirm = PasswordField('confirm',
                            filters=[strip_filter])


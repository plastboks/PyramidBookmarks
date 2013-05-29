from wtforms import (
  Form,
  BooleanField,
  TextField,
  TextAreaField,
  validators,
  HiddenField,
  )

strip_filter = lambda x: x.strip() if x else None

class BookmarkCreateForm(Form):
  title = TextField('Bookmark title',
                    [validators.Length(min=1, max=255)],
                    filters=[strip_filter])
  url = TextField('Bookmark URL',
                      [validators.Length(min=1, max=512)],
                      filters=[strip_filter])

class BookmarkUpdateForm(BookmarkCreateForm):
  id = HiddenField()

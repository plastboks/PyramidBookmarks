<%! from pyramid.security import authenticated_userid %>
% if authenticated_userid(request):
<form action="/search" method="GET">
  <label for="q">Search</label>
%if request.params.get('q') and type is not 'tag':
  <input name="q" value="${ request.params.get('q', '') }" type="text"/>
%else:
  <input name="q" value="" type="text"/>
%endif
  <input type="submit" value="Search" />
</form>
% if request.params.get('q') and type is not 'tag':
  <a href="/index">Reset search</a>
% endif
% endif

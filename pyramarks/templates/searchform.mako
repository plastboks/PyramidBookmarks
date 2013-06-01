<form action="/search" method="GET">
  <label for="q">Search</label>
  <input name="q" value="${ request.params.get('q', '') }" type="text"/>
  <input type="submit" value="Search" />
</form>
% if request.params.get('q'):
  <a href="/index">Reset search</a>
% endif

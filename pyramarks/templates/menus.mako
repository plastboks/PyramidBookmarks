<%! from pyramid.security import authenticated_userid %>
% if authenticated_userid(request):
<div id="primenu">
  <ul>
    <li><a href="${request.route_url('index')}">Home</a></li>
    <li><a href="${request.route_url('logout')}">Logout</a></li>
  </ul>
</div>
<div id="secmenu">
  <ul>
    <li><a href="${request.route_url('bookmark_action',action='create')}">Create a new bookmark</a></li>
  </ul>
</div>
% endif

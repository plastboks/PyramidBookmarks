<%! from pyramid.security import authenticated_userid %>
<div id="primenu">
  <ul>
% if authenticated_userid(request):
    <li><a href="${request.route_url('index')}">Home</a></li>
    <li><a href="${request.route_url('profile')}">Profile</a></li>
    <li><a href="${request.route_url('logout')}">Logout</a></li>
% else:
    <li><a href="${request.route_url('login')}">Login</a></li>
    <li><a href="${request.route_url('register')}">Register</a></li>
% endif
  </ul>
</div>
% if authenticated_userid(request):
<div id="secmenu">
  <ul>
    <li><a href="${request.route_url('bookmark_action',action='create')}">Create a new bookmark</a></li>
  </ul>
</div>
% endif

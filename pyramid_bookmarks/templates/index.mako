<%inherit file="pyramid_bookmarks:templates/base.mako"/>
<%
from pyramid.security import authenticated_userid
user_id = authenticated_userid(request)
%>
% if user_id:
    Welcome <strong>${user_id}</strong> ::
    <a href="${request.route_url('logout')}">Sign Out</a>
%endif

% if paginator.items:

    ${paginator.pager()}

    <h2>Bookmarks</h2>

    <ul>
    % for entry in paginator.items:
    <li>
    <a href="${request.route_url('bookmark', id=entry.id, slug=entry.slug)}">
    ${entry.title}</a>
    </li>
    % endfor
    </ul>

    ${paginator.pager()}

% else:

<p>No bookmarks found.</p>

%endif

<p><a href="${request.route_url('bookmark_action',action='create')}">
Create a new bookmark</a></p>

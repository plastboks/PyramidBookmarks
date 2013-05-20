<%inherit file="pyramid_bookmarks:templates/base.mako"/>

Welcome <strong>${username}</strong> ::
<a href="${request.route_url('logout')}">Sign Out</a>

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

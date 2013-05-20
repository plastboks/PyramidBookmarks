<%inherit file="pyramid_bookmarks:templates/base.mako"/>

<h1>${bookmark.title}</h1>
<hr/>
<p>${bookmark.url}</p>
<hr/>
<p>Created <strong title="${bookmark.created}">
${bookmark.created_in_words}</strong> ago</p>

<p><a href="${request.route_url('home')}">Go Back</a> ::
<a href="${request.route_url('bookmark_action', action='edit',
_query=(('id',bookmark.id),))}">Edit Bookmark</a> :: 
<a href="${request.route_url('bookmark_action', action='delete',
_query=(('id',bookmark.id),))}">Delete Bookmark</a>
</p>

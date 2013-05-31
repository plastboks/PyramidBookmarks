<%inherit file="pyramarks:templates/base.mako"/>

% if paginator.items:

    <h1>My bookmarks</h1>

    <div class="bookmarksbox">
      <table class="bookmarks">
        <thead>
            <th>Title</th>
            <th>Clicks</th>
            <th>Action</th>
        </thead>
        <tbody>
          % for bookmark in paginator.items:
                <tr>
                    <td class='titlecolumn'>
                        <a href="${ bookmark.url }" class="clickIncrement" target="_blank" title="${ bookmark.title }" rel="noreferrer">
                          ${ bookmark.title }
                        </a><br />
                        % if bookmark.tags:
                          % for w in bookmark.tags.split(' '):
                            <a href="" class="tag">${w}</a>
                          % endfor
                        % endif
                    </td>
                    <td class="clickscolumn">
                      <span>0</span>
                    </td>
                    <td class='actioncolumn'>
                      <a href="${request.route_url('bookmark_action', action='edit', _query=(('id',bookmark.id),))}">
                        Edit
                      </a> 
                      <a href="${request.route_url('bookmark_action', action='delete', _query=(('id',bookmark.id),))}">
                        Delete
                      </a>
                    </td>
                </tr>
          % endfor
        </tbody>
      </table>
    </div>


    ${paginator.pager()}

% else:

  <p>No bookmarks found.</p>

%endif


<%inherit file="pyramarks:templates/base.mako"/>

<div id="bookmarkedit">
  <h1>Add a new bookmark</h1>

  <form action="${request.route_url('bookmark_action',action=action)}" method="post">

    %if action =='edit':
      ${form.id()}
    %endif

    % for error in form.title.errors:
      <div class="error">${ error }</div>
    % endfor

    <p>
      <label>${form.title.label}</label><br />
      ${form.title()}
    </p>

    % for error in form.url.errors:
      <div class="error">${error}</div>
    % endfor

    <p>
      <label>${form.url.label}</label><br />
      ${form.url()}
    </p>

    <p>
      <input type="submit" value="Submit">
    </p>

  </form>
</div>

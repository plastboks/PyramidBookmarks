<%inherit file="pyramarks:templates/base.mako"/>

<div id="bookmarkedit">
  <form action="${request.route_url('bookmark_action',action=action)}" method="post">
    %if action =='edit':
      ${form.id()}
    %endif

    % for error in form.title.errors:
        <div class="error">${ error }</div>
    % endfor

    <div>
      <label>${form.title.label}</label>
      ${form.title()}
    </div>

    % for error in form.url.errors:
    <div class="error">${error}</div>
    % endfor

    <div>
      <label>${form.url.label}</label>
      ${form.url()}
    </div>
    <div>
      <input type="submit" value="Submit">
    </div>
  </form>
</div>
<p>
  <a href="${request.route_url('index')}">Go Back</a>
</p>

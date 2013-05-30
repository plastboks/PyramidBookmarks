<%inherit file="pyramarks:templates/base.mako"/>

<h1>Register</h1>
<div id="register">
  <form action="${request.route_url('register')}" method="POST">
    <p>
      % for error in form.username.errors:
        <div class="error">${ error }</div>
      % endfor
      <label>${form.username.label}</label><br />
      ${form.username()}
    </p>
    <p>
      % for error in form.email.errors:
        <div class="error">${ error }</div>
      % endfor
      <label>${form.email.label}</label><br />
      ${form.email()}
    </p>
    <p>
      % for error in form.password.errors:
        <div class="error">${ error }</div>
      % endfor
      <label>${form.password.label}</label><br />
      ${form.password()}
    </p>
    <p>
      <label>${form.confirm.label}</label><br />
      ${form.confirm()}
    </p>
      <input type="submit" value="Register" />
  </form>
</div>

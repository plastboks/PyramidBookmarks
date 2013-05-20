<%inherit file="pyramid_bookmarks:templates/base.mako"/>
<div id="login">
  <form action="${request.route_url('login')}" method="post">
    <p>
      <label>User</label>
      <input type="text" name="username">
    </p>
    <p>
      <label>Password</label>
      <input type="password" name="password">
    </p>
      <input type="submit" value="Sign in">
  </form>
</div>

<!DOCTYPE HTML>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
  <title>Bookmarkapp - ${title} </title>
  <link rel="shortcut icon" href="${request.static_url('pyramarks:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyramarks:static/css/normalize.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pyramarks:static/css/style.css')}" type="text/css" media="screen" charset="utf-8" />

  <script src="${request.static_url('pyramarks:static/js/jquery-2.0.1.min.js')}" type="text/javascript"></script>
  <script src="${request.static_url('pyramarks:static/js/commons.js')}" type="text/javascript"></script>
</head>
<body>

  <div id="header">
    <%include file="pyramarks:templates/menus.mako"/>
  </div>
  <div id="content">
      ${next.body()}
  </div>
  <div id="footer">My awesome pyramid bookmark app</div>

</html>

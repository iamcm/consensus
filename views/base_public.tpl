
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Site</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
        <link href="/static/css/bootstrap.css" rel="stylesheet">
        <style>
            body {
                padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
            }
        </style>
        <link href="{{vd['baseurl']}}/static/css/bootstrap-responsive.css" rel="stylesheet">
        <link href="{{vd['baseurl']}}/static/css/generic.css" rel="stylesheet">
        %if defined('css'):
            %css()
        %end
            
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
    
        <link rel="shortcut icon" href="{{vd['baseurl']}}/static/ico/favicon.ico">
        <link rel="apple-touch-icon-precomposed" sizes="144x144" href="{{vd['baseurl']}}/static/ico/apple-touch-icon-144-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="114x114" href="{{vd['baseurl']}}/static/ico/apple-touch-icon-114-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="72x72" href="{{vd['baseurl']}}/static/ico/apple-touch-icon-72-precomposed.png">
        <link rel="apple-touch-icon-precomposed" href="{{vd['baseurl']}}/static/ico/apple-touch-icon-57-precomposed.png">
    </head>
  
    <body>

        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container-fluid">
                    <a class="brand" href="{{vd['baseurl']}}/">Consensus</a>
                    
                    <div class="nav-collapse collapse right">
                        <ul class="nav">
                        </ul>
                    </div>
                    
                </div>
            </div>
        </div>
    
        <div>
            %include
        </div>
        
        %if defined('js'):
            %js()
        %end
        
    </body>
</html>

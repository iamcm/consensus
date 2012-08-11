%setdefault('email','')
%setdefault('password','')

<div class="container-fluid p10">
    
    %if defined('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{error}}
    </div>
    %end

    <form class="form-horizontal" id="loginForm" method='POST' action="/login" >
        
        <div class="control-group">
            <div class="controls">
                <input type="text" class="input-xlarge" name="email" id="email" value="{{email}}" placeholder="Email" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <input type="password" class="input-xlarge" name="password" id="password" value="{{password}}" placeholder="Password" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn">Login</button>
                or <a href="/register">register an account</a>
            </div>
        </div>
        
    </form>
    
    <div class="fblogin">
        <p>Or:</p>
        <a href="/fb/login" class="btn"><img src="/static/img/f_logo.png" /> Login in with Facebook</a>
    </div>
</div>

%def js():
<script>
    $('#email').focus();
</script>
%end

%def css():
<style>
    .fblogin
    {
        border-top: 1px solid #ddd;
        padding-top:20px;
    }
    .fblogin img
    {
        width:20px;   
    }
</style>
%end

%rebase base_public css=css, js=js
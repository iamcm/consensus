%setdefault('email','')
%setdefault('password1','')
%setdefault('password2','')

<div class="container-fluid p10">
    
    %if defined('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{error}}
    </div>
    %end

    <form class="form-horizontal" id="registerForm" method='POST' action="" >
        
        <div class="control-group">
            <label class="control-label" for="email">Email</label>
            <div class="controls">
                <input type="text" class="input-xlarge" name="email" id="email" value="{{email}}" />
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label" for="password1">Password</label>
            <div class="controls">
                <input type="password" class="input-xlarge" name="password1" id="password1" value="{{password1}}" />
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label" for="password2">Password again</label>
            <div class="controls">
                <input type="password" class="input-xlarge" name="password2" id="password2" value="{{password2}}" />
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn">Create account</button>
            </div>
        </div>
        
    </form>
</div>

%rebase base_public vd=vd
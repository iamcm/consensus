
<div class="container-fluid p10">
    
    %if vd.get('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{vd.get('error')}}
    </div>
    %end

    <form class="form-horizontal" method='POST' action="" >

        %if vd['q']._id:
        <input type="hidden" name="_id" value="{{vd['q']._id}}" />
        %end
        
        <div class="control-group">
            <label class="control-label" for="text">Text</label>
            <div class="controls">
                <input type="text" class="input-xlarge" id="text" name="text" value="{{vd['q'].text if vd['q'].text else ''}}">
            </div>
        </div>
        
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn">Save</button>
            </div>
        </div>
        
    </form>
</div>

%def js():
<script>
    $('#text').focus();
</script>
%end


%rebase base js=js
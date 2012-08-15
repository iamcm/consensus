
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
            <label class="control-label" for="text">
                Options
                <br />
                <a href="#" id='addOption'>Add option</a>
            </label>
            <div class="controls options">
                <p><input type="text" class="input-xlarge" name="option"></p>
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
<script id="tplOption" type="text/x-handlebars-template">
    <p>
        <input type="text" class="input-xlarge" name="option">
    </p>
</script>

<script>
    $('#text').focus();

    $('#addOption').click(add_option);

    var new_option = Handlebars.compile($("#tplOption").html());

    function add_option () {
        $('.options').append(new_option);
    }
</script>
%end


%rebase base js=js, vd=vd
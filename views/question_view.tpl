
<div class="container-fluid p10">
    
    <h3>
        {{vd['q'].text}}
    </h3>

    <form class="form-horizontal" method='POST' action="{{vd['baseurl']}}/question/respond" >

        <input type="hidden" name="_id" value="{{vd['q']._id}}" />
        
        <div class="control-group">
            <label class="control-label" for="text">
                Options
            </label>
            <div class="controls options">
                %for o in vd['q'].options:
                <p><input type="radio" name="option" value="{{o._id}}" /> {{o.text}}</p>
                %end
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

%end


%rebase base js=js, vd=vd

<div class="container">
    %for c in vd['cons']:
    <div class="row">
        <a href="{{vd['baseurl']}}/question?_id={{c._id}}">{{c.text}}</a>
    </div>
    %end
</div>


%def js():
    
%end

%rebase base js=js, vd=vd
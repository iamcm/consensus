
<div class="container">
    %for q in vd['questions']:
    <div class="row">
        <a href="{{vd['baseurl']}}/question/view?_id={{q._id}}">{{q.text}}</a>
        <span class="right">
            <a href="{{vd['baseurl']}}/question?_id={{q._id}}">edit</a>
            |
            <a href="{{vd['baseurl']}}/question/delete?_id={{q._id}}">delete</a>
        </span>
    </div>
    %end
</div>


%def js():
    
%end

%rebase base js=js, vd=vd
$(function(){
if('{{question.status}}'=='True'){
    $('input[id="{{question.option_selected}}"]').prop("checked", true);
    $('span[id="{{question.option_selected}}"]').html('<i class="fa fa-check" style="color: green;"></i>');
    $('input[name="questionradio"]').attr("disabled",true);
}else if('{{question.status}}'=='False'){
    $('input[id="{{question.option_selected}}"]').prop("checked", true);
    $('span[id="{{question.option_selected}}"]').html('<i class="fa fa-remove" style="color: red;"></i>');
}
$("#quizsubmit").on('click',function(){
    var question = '{{question.status}}';
    alert(question);
    var answer=$('input[name="questionradio"]:checked').val();
    if(answer){
    $('#error').html('');
    $("#quizsubmit").html("submittining...");
    $('span[name="questionspan"]').html("");
    $.ajax({
        url : "/quiz_submit/", // the endpoint
        type : "POST", // http method
        data : { code:"{{question.code}}",
                answer:$('input[name="questionradio"]:checked').val()}, // data sent with the post request
    // handle a successful response
        success : function(json) {
        if(json['status']){
            $("span[id="+answer+"]").html('<i class="fa fa-check" style="color: green;"></i>');
            $('#status').html('<i class="fa fa-check" style="color: green;"></i>');
            $('input[name="questionradio"]').attr("disabled",true);
            $('#quizsubmit').removeClass("btn-primary");
            $('#quizsubmit').addClass("btn-success disabled");
            $('#quizsubmit').html("Accepted");
        }
        else{
            $("span[id="+answer+"]").html('<i class="fa fa-remove" style="color: red;"></i>');
            $('#status').html('<i class="fa fa-remove" style="color: red;"></i>');
            $("#quizsubmit").html("Submit");
        }
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
        alert(response["responseJSON"]["error"]);
    }
    });
    }
    else{
    $('#error').html("please select an option");
    }
});
});
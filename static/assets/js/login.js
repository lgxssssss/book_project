$(function(){
    $("#input_username").blur(function(){
        var input_username = $(this).val();
        $.post("query_user",
    {
        username:input_username,
    },
    function(data,status){
        if(status ="sucess"){
            if(data["code"] == 0){
            }else{
                $("#user_status").text("用户不存在").css("color","red");
                $("#user_status").show();
            }
        }
    });
    });

    $("#login").click(function(){
        var input_password = $("#input_password").val();
        var input_username = $("#input_username").val();
        console.log(input_username);
        console.log(input_password);

        $.post("query_login",
    {
        username:input_username,
        password:input_password,
    },
    function(data,status){
        if(status ="sucess"){
            console.log("sucess");
            if(data["code"] == 0){
                // window.location.href="/home";
                window.location.href='/'
            }if(data["code"] == -1){
                console.log("用户不存在");
            }else{
                console.log("password is worring!!");
            }
                
            }
        }
        ) 
    });

});

$(function(){
    $("#register").click(function(){
        var input_password = $("#input_password").val();
        var input_username = $("#input_username").val();
        $.post("/query_register",
    {
        username:input_username,
        password:input_password,
    },
    function(data,status){
        if(status ="sucess"){
            console.log("sucess");
            if(data["code"] == 0){
                window.location.href='/login'
                alert("注册成功，请登录！")
            }else{
                console.log("password is worring!!");
            }
                
            }
        }
        ) 
    });

});
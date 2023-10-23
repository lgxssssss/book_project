$(function(){
    $("#book_create").click(function(){
        var input_bookname = $("#input_bookname").val();
        var input_price = $("#input_price").val();
        var picture = $("#picture").val();
        var book_desc = $("#book_desc").val();
        console.log(picture)
        $.post("/book_create_quary",
    {
        book_name:input_bookname,
        price:input_price,
        picture:picture,
        book_desc:book_desc,
    },
    function(data,status){
        if(status ="sucess"){
            console.log("sucess");
            if(data["code"] == 0){
                window.location.href='/'
                alert("创建图书成功！")
            }else{
                console.log("创建图书失败!!");
            }
                
            }
        }
        ) 
    });

});
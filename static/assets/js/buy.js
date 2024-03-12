$(function(){
    $("#btn").click (function(){

        var book_id = $("#book_id").val();
        console.log(book_id);

        $.post("/query_buy",
    {
        book_id:book_id,
    },
    function(data,status){
        if(status ="sucess"){
            console.log("sucess");
            if(data["code"] === 0){
                alert("购买成功！！");
                window.location.href='/order';
            }else{
                alert("购买失败！！")
            }
        }
        
    });
    });
});
$(function(){
    $(".aaa").click(function(){
        var oid = $(this).attr("id");
        var aa = $(this);
        $.post("/query_order_delect",
    {
        oid:oid,
    },
    function(data,status){
        if(status ="sucess"){
            if(data["code"] === 0){                
                aa.parent().parent().remove();
            }      
            }
        }
        ) 
    });

});
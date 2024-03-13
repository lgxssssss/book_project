$(function(){
    $(".aaa").click(function(){
        var id = $(this).attr("id");
        var aa = $(this);
        $.post("/query_book_delect",
    {
        id:id,
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
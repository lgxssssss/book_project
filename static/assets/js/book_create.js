$(function(){
    $("#book_create").click(function(){
        var input_bookname = $("#input_bookname").val();
        var input_price = $("#input_price").val();
        var book_desc = $("#book_desc").val();
        // var fileObj = $("FileUpload").files[0];
        var fileObj = document.getElementById("FileUpload").files[0]
        // alert("点击成功")

        if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
            alert("还没选择图片，请选择图片");
            return;}

        var formFile = new FormData();
        formFile.append("action", "UploadVMKImagePath");  
        formFile.append("book_name", input_bookname);
        formFile.append("price", input_price);
        formFile.append("file", fileObj);
        formFile.append("book_desc", book_desc);
        var data = formFile;
        console.log(input_bookname,input_price,fileObj,book_desc)
        // alert("请选择图片,停止1")

    //     $.post("/book_create_quary",
    // {
    //     // book_name:input_bookname,
    //     // price:input_price,
    //     // book_desc:book_desc,
    //     // file: fileObj,
    //     data: data,
    //     dataType: "json",
    //     cache: false,//上传文件无需缓存
    //     processData: false,//用于对data参数进行序列化处理 这里必须false
    //     contentType: false, //必须
    // },
    // function(data,status){
    //     if(status ="sucess"){
    //         console.log("sucess");
    //         if(data["code"] == 0){
    //             window.location.href='/'
    //             alert("创建图书成功！")
    //         }if(data["code"] == -1){
    //             alert("书名有问题")
    //         }if(data["code"] == -2){
    //             alert("没传入图片")
    //         }if(data["code"] == -3){
    //             alert("图片名为空")
    //         }else{
    //             console.log("创建图书失败!!");
    //         }
                
    //         }
    //     }
    //     ) 
                $.ajax({
                    url: "/book_create_quary",
                    data: data,
                    type: "Post",
                    dataType: "json",
                    cache: false,//上传文件无需缓存
                    processData: false,//用于对data参数进行序列化处理 这里必须false
                    contentType: false, //必须
                    success: function (result) {
                        window.location.href='/';
                        alert("上传完成!");
                    },
                })
    });

});
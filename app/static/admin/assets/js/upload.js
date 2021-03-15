//文件上传本地
var opts = {
    url: "/admin/photos",
    type: "POST",
    success: function (data) {
        console.log(data)
        $("input[name='image']").val(data.image_url);
        $("#img_show").attr("src", data.image_url);
    },
    error: function () {
        alert('文件上传失败');
    }
};

$('#image_upload').fileUpload(opts);


//文件上传七牛
var qiniu = {
    url: "/admin/upload_qiniu",
    type: "POST",
    success: function (data) {
        console.log(data)
        $("input[name='image']").val(data.image_url);
        $(".img_show").attr("src", data.image_url);
    },
    error: function () {
        alert('文件上传失败');
    }
};

$('.image_upload').fileUpload(qiniu);
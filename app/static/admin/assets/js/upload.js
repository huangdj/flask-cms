//文件上传
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
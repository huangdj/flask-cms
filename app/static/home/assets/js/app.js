$(document).ready(
    function () {
        $.foucs({direction: 'left'});

        $(".d_1200 li").mouseover(function () {
            $(this).find(".z1 a").css("color", "#737578")
        });
        $(".d_1200 li").mouseout(function () {
            $(this).find(".z1 a").css("color", "#585858")
        });

        $(".wx .z3").mouseover(function () {
            $(this).find(".pf").show();
        });
        $(".wx .z3").mouseout(function () {
            $(this).find(".pf").hide();
        });
    });

$(document).ready(
    function () {
        $(".d_1200 li").mouseover(function () {
            var _en = $(this).find(".z1 a").attr("_en");
            $(this).find(".z1 a").html(_en);
            // $(this).find(".z1 a").css("color", "#2aa8e2");
            $(this).find(".z1 .z_2 a").css("color", "#999999");
        });

        $(".d_1200 li").mouseout(function () {
            var _cn = $(this).find(".z1 a").attr("_cn");
            $(this).find(".z1 a").html(_cn);
            $(this).find(".z1 a").css("color", "#585858");
            $(this).find(".z1 .z_2 a").css("color", "#999999");
        });
    });

var s_count = $(".pz_slides_3 ._pic img").length;
var s_li = "";
for (j = 1; j <= s_count; j++) {
    s_li += "<li></li>";
}
$(".pz_slides_3 > ._btn").html("<ul>" + s_li + "</ul>");
jQuery(".pz_slides_3").slide({
    titCell: "._btn li",
    mainCell: "._pic ul",
    effect: "fold",
    autoPlay: true,
    delayTime: 1500,
    interTime: 6000
});
$("#nav1").addClass("on");


$(function () {
  $(".sideList").on("click", "li", function () {
    var sId = $(this).data("id"); //获取data-id的值
    window.location.hash = sId; //设置锚点
    loadInner(sId);
  });

  function loadInner(sId) {
    var sId = window.location.hash;
    var pathn, i;
    switch (sId) {
      case "#guesture":
        pathn = "../static/guesture.html";
        i = 0;
        break;
      case "#pose":
        pathn = "../static/pose.html";
        i = 1;
        break;
      case "#face":
        pathn = "../static/face.html";
        i = 2;
        break;
      case "#down":
        pathn = "../static/down.html";
        i = 3;
        break;
      default:
        pathn = "./guesture.html";
        i = 0;
        break;
    }
    // $("#content").empty();
    $("#content").load(pathn); //加载相对应的内容
    $(".sideList li").eq(i).addClass("active").siblings().removeClass("active"); //当前列表高亮
  }
  var sId = window.location.hash;
  loadInner(sId);
});

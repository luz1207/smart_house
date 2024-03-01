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
      case "#home":
        pathn = "./home.html";
        i = 0;
        break;
      case "#guesture":
        pathn = "./guesture.html";
        i = 1;
        break;
      case "#pose":
        pathn = "./pose.html";
        i = 2;
        break;
      case "#tod":
        pathn = "./.html";
        i = 3;
        break;
      case "#down":
        pathn = "./down.html";
        i = 4;
        break;
      default:
        pathn = "./home.html";
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

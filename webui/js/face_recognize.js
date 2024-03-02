var percent = 80;
// 1.canvas实现
circle()
function circle() {
    var canvas = document.getElementById('circle');
    var ctx = canvas.getContext("2d");

    /*填充文字*/

    ctx.font = "12px Microsoft YaHei";
    /*文字颜色*/
    ctx.fillStyle = '#F1090B';
    /*文字内容*/
    var insertContent = '匹配度';
    var text = ctx.measureText(insertContent);
    /*插入文字，后面两个参数为文字的位置*/
    /*此处注意：text.width获得文字的宽度，然后就能计算出文字居中需要的x值*/
    ctx.fillText(insertContent, (132 - text.width) / 2, 68);

    /*填充百分比*/
    var ratioStr = percent + '%';
    var text = ctx.measureText(ratioStr);
    ctx.fillText(ratioStr, (132 - text.width) / 2, 85);

    /*开始圆环*/
    var circleObj = {
        ctx: ctx,
        /*圆心*/
        x: 66,
        y: 66,
        /*半径*/
        radius: 40,
        /*环的宽度*/
        lineWidth: 10
    }

    /*有色的圆环*/
    /*从-90度的地方开始画*/
    circleObj.startAngle = - Math.PI * 2 * 90 / 360;
    /*从当前度数减去-90度*/
    circleObj.endAngle = Math.PI * 2 * (percent / 100 - 0.25);
    circleObj.color = '#F1090B';
    drawCircle(circleObj);

    /*灰色的圆环*/
    /*开始的度数-从上一个结束的位置开始*/
    circleObj.startAngle = circleObj.endAngle;
    /*结束的度数*/
    circleObj.endAngle = Math.PI * 2;
    circleObj.color = '#ff453833';
    drawCircle(circleObj);

}
/*画曲线*/
function drawCircle(circleObj) {
    var ctx = circleObj.ctx;
    ctx.beginPath();
    ctx.arc(circleObj.x, circleObj.y, circleObj.radius, circleObj.startAngle, circleObj.endAngle, false);
    //设定曲线粗细度
    ctx.lineWidth = circleObj.lineWidth;
    //给曲线着色
    ctx.strokeStyle = circleObj.color;
    //连接处样式
    ctx.lineCap = 'round';
    //给环着色
    ctx.stroke();
    ctx.closePath();
}
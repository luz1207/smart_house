// 定义一些变量
var name = '未知';//匹配到人脸的名字，未检测成功显示未知
var gender = '未知';//匹配到人脸的性别
var recognize_status = '正在验证';
var percent = 80;

circle()
//实现画出圆形匹配度功能
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

//获取当前时间
const divObj=document.getElementsByClassName('show_time')[0];
    setInterval(()=>{
        const nowTime=getNowTime();
        divObj.innerText=nowTime;
    })

function getNowTime(){
    const date=new Date();
    const year=date.getFullYear();
    const month=date.getMonth()+1;
    const day=date.getDate();
    const hour=date.getHours();
    const minite=date.getMinutes();
    const seconds=date.getSeconds();
    return `${year}-${month}-${day} ${hour}:${minite}:${seconds<10?'0'+seconds:seconds}`
}

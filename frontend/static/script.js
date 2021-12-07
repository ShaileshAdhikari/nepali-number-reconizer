var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
var curX, curY, prevX, prevY;
var hold = false;
ctx.lineWidth = 5;
var canvas_data = {"pencil": [],}
               
function reset(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas_data = { "pencil": [] }
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // $("#resultHolder").hide();
    // $("#divClassTable").hide();
}
        
// pencil tool
        
function pencil(){
        
    canvas.onmousedown = function(e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function(e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
        
    canvas.onmouseup = function(e){
        hold = false;
    };
        
    canvas.onmouseout = function(e){
        hold = false;
    };
        
    function draw(){
        ctx.lineTo(curX, curY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}

function identify(){
        const toTimestamp = (strDate) => {
            const dt = Date.parse(strDate);
            return parseInt(dt / 1000);
        }
    var filename = toTimestamp(new Date().toLocaleString()) + ".png";
    var data = JSON.stringify(canvas_data);
    var image = canvas.toDataURL();
    
    $.post("/", {
        save_fname: filename, save_cdata: data, save_image: image
    },function (data, status){
        console.log(data);
        let numbers = ['zero','one','two','three','four','five','six','seven','eight','nine'];

        $("#resultHolder").html(numbers[data.classVal]);
        $("#result-image-holder").html("<img src=" +data.path+ "/>")
        let confDict = data.class_prob[0];
        for (let i=0;i < confDict.length; i++){
            let elementName = "#score_"+numbers[i];
            $(elementName).html((confDict[i]*100).toFixed(10) + " %");
        }
        $("#resultHolder").show();
        $("#divClassTable").show();
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    // $("#resultHolder").hide();
    // $("#divClassTable").hide();
});
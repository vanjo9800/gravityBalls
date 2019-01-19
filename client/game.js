var engineSocket = new WebSocket("ws://localhost:8765");

function circle() {
    this.x = 0;
    this.y = 0;
    this.r = 10;
    this.dx = 0;
    this.dy = 0;
    this.move = function () {
        this.x += this.dx;
        this.y += this.dy;
    };
    this.moveBack = function () {
        this.x += this.dx;
        this.y += this.dy;
    };
    this.draw = function () {
        context.beginPath();
        context.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
        context.fillStyle = "white"; //Circles colour
        context.fill();
        context.closePath();
    };
    this.collidingWith = function (b) {
        return (b.x - this.x) * (b.x - this.x) + (b.y - this.y) * (b.y - this.y) < (b.r + this.r) * (b.r + this.r);
    };
}

var circles = [];
engineSocket.onmessage = function (event) {
    circles = [];
    var balls = JSON.parse(event.data);
    for (var i = 0; i < balls.length; i++) {
        circles[i] = new circle();
        circles[i].x = balls[i].x;
        circles[i].y = balls[i].y;
        circles[i].r = balls[i].r;
    }
    console.log(balls);
}

var width = window.innerWidth;
var height = window.innerHeight;
var startedGame = false;
//var clicked = false;


// var initNumber = 30;
// for (var i = 0; i < initNumber; i++) {
//     circles[i] = new circle();
//     circles[i].x = Math.random() * width;
//     circles[i].y = Math.random() * height;
//     circles[i].r = Math.random() * 20 + 10;
//     circles[i].dx = Math.random() * 10 + 3;
//     circles[i].dy = Math.random() * 10 + 3;
// }


function update() {
    if (!startedGame) return;
    // for (var i = 0; i < initNumber; i++) {
    //     circles[i].move();
    //     if (circles[i].y + circles[i].r > canvas.height) {
    //         circles[i].y = canvas.height - circles[i].r;
    //         circles[i].dy = -circles[i].dy;
    //     }
    //     if (circles[i].y + circles[i].r < 0) {
    //         circles[i].y = circles[i].r;
    //         circles[i].dy = -circles[i].dy;
    //     }
    //     if (circles[i].x + circles[i].r > canvas.width) {
    //         circles[i].x = canvas.width - circles[i].r;
    //         circles[i].dx = -circles[i].dx;
    //     }
    //     if (circles[i].x + circles[i].r < 0) {
    //         circles[i].x = circles[i].r;
    //         circles[i].dx = -circles[i].dx;
    //     }
    //     var collision = false;
    //     for (var j = 0; j < initNumber; j++) {
    //         if (i == j) continue;
    //         if (circles[i].collidingWith(circles[j])) {
    //             collision = true;
    //         }
    //     }
    //     if (collision) circles[i].moveBack();
    // }
}

function draw() {
    if (!startedGame) return;

    context.fillStyle = "black";
    context.fillRect(0, 0, canvas.width, canvas.height);
    // if (!clicked) {
    //     canvas.style.webkitFilter = "blur(10px)";
    //     return;
    // } else {
    //     canvas.style.webkitFilter = "blur(0px)";
    // }
    for (var i = 0; i < circles.length; i++) {
        circles[i].draw();
    }
}

function clearScreen() {
    document.getElementById("startscreen").style.display = "none";
    document.getElementById("gamescreen").style.display = "block";
    startedGame = true;
}

function keyup(key) {
    // Show the pressed keycode in the console
}

function mouseup() {
    // Show coordinates of mouse on click
}
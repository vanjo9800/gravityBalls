var ws_link = "ws://" + window.location.hostname + ":8765";
console.log(ws_link);
var engineSocket = new WebSocket(ws_link);
var startedGame = false;

function calculateColour (id) {
    var r = parseInt(id*13753/4) % 206 + 50;
    var g = parseInt(id*25732/5) % 206 + 50;
    var b = parseInt(id*36294/2) % 206 + 50;
    return "rgb(" + r + "," + g + "," + b +")";
}

function circle() {
    this.x = 0;
    this.y = 0;
    this.r = 10;
    this.dx = 0;
    this.dy = 0;
    this.dr = 0;
    this.dt = 0;
    this.score = 0;
    this.move = function () {
        if (this.dt <= 0.0) return;
        this.x += this.dx;
        this.y += this.dy;
        this.r += this.dr;
        this.dt--;
    };
    this.draw = function (id) {
        context.beginPath();
        context.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
        context.fillStyle = calculateColour(id); //Circles colour
        context.fill();
        context.closePath();
    };
    this.collidingWith = function (b) {
        return (b.x - this.x) * (b.x - this.x) + (b.y - this.y) * (b.y - this.y) < (b.r + this.r) * (b.r + this.r);
    };
}

var circles = [],
    lastTimestamp = 0;
engineSocket.onmessage = function (event) {
    circles = [];
    if (event.data == "s") {
        startGame();
        return;
    }
    if (event.data.startsWith("i")) {
        console.log(event.data.substring(1));
        var id = parseInt(event.data.substring(1));
        console.log(id);
        var nodecolour = calculateColour(id);
        console.log(nodecolour);
        document.getElementById("title-text").style.color = nodecolour;
        return;
    }

    var currentTimestamp = new Date().getMilliseconds();
    var dt = (currentTimestamp - lastTimestamp) / 20; //update run interval
    var balls = JSON.parse(event.data);
    if (startGame) {
        for (var i = 0; i < balls.length; i++) {
            if (circles[balls[i].id] == undefined) {
                circles[balls[i].id] = new circle();
                circles[balls[i].id].x = balls[i].x;
                circles[balls[i].id].y = balls[i].y;
                circles[balls[i].id].r = balls[i].r;
            } else {
                circles[balls[i].id].dx = (balls[i].x - circles[balls[i].id].x) / dt;
                circles[balls[i].id].dy = (balls[i].y - circles[balls[i].id].y) / dt;
                circles[balls[i].id].dr = (balls[i].r - circles[balls[i].id].r) / dt;
                circles[balls[i].id].dt = dt;
            }
            circles[balls[i].id].score = balls[i].s;
        }
        lastTimestamp = currentTimestamp;
    }
}

function requestStart() {
    engineSocket.send("s");
}

function update() {
    if (!startedGame) return;
    for (var id in circles) {
        circles[id].move();
    }
    if (isKeyPressed[38]) { //up
        console.log("up")
        engineSocket.send("+");
        isKeyPressed[38] = false;
    }
    if (isKeyPressed[40]) { //down
        engineSocket.send("-");
        isKeyPressed[40] = false;
    }
}

function draw() {
    if (!startedGame) return;

    context.fillStyle = "black";
    context.fillRect(0, 0, 900, 900);

    context.beginPath();
    context.arc(450, 450, 449, 0, 2.0 * Math.PI, false);
    context.lineWidth = 2;
    context.strokeStyle = '#FFFFFF';
    context.stroke();

    // if (!clicked) 
    //     canvas.style.webkitFilter = "blur(10px)";
    //     return;
    // } else {
    //     canvas.style.webkitFilter = "blur(0px)";
    // }
    var keys = Object.keys(circles).sort();
    for (var i = 0; i < keys.length; i++) {
        context.font = "120px Courier New";
        context.globalAlpha = 0.5;
        context.fillStyle = calculateColour(keys[i]);
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillText(circles[keys[i]].score.toString(), (0.5 + parseFloat(i))*(900.0 / parseFloat(keys.length)), 450); 
        console.log(parseFloat(i), keys.length);
        console.log((0.5 + parseFloat(i)) * 900.0 / parseFloat(keys.length)); 
    }

    for (var id in circles) {
        circles[id].draw(id);
    }
}

function startGame() {
    console.log("start");
    document.getElementById("startscreen").style.display = "none";
    startedGame = true;
}

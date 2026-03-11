"""
NEXAH Pattern Explorer Web
==========================

Run:
    python ENGINE/nexah_kernel/demos/nexah_pattern_explorer_web.py

Open browser:
    http://127.0.0.1:8000
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "127.0.0.1"
PORT = 8000


INDEX_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>NEXAH Pattern Explorer</title>

<style>

body{
margin:0;
font-family:Arial;
background:#111;
color:#eee;
}

.wrap{
display:grid;
grid-template-columns:320px 1fr;
min-height:100vh;
}

.sidebar{
padding:20px;
background:#1a1a1a;
border-right:1px solid #333;
}

.main{
padding:16px;
}

h1{
margin-top:0;
font-size:22px;
}

.control{
margin-bottom:18px;
}

label{
display:block;
margin-bottom:6px;
}

.value{
font-family:monospace;
color:#8fd;
}

canvas{
background:#000;
border:1px solid #333;
}

button{
background:#333;
color:#fff;
border:0;
padding:8px 12px;
cursor:pointer;
}

</style>
</head>

<body>

<div class="wrap">

<div class="sidebar">

<h1>NEXAH Explorer</h1>

<div class="control">
<label>Symmetry n</label>
<input type="range" min="3" max="20" value="7" id="n">
<div class="value" id="n_val"></div>
</div>

<div class="control">
<label>Drift (deg)</label>
<input type="range" min="0" max="6" step="0.01" value="0" id="drift">
<div class="value" id="d_val"></div>
</div>

<div class="control">
<label>Iterations</label>
<input type="range" min="100" max="4000" step="50" value="2000" id="iter">
<div class="value" id="i_val"></div>
</div>

<div class="control">
<label>Radius</label>
<input type="range" min="2" max="8" step="0.1" value="5" id="radius">
<div class="value" id="r_val"></div>
</div>

<button onclick="savePNG()">Save PNG</button>

</div>

<div class="main">

<canvas id="canvas" width="900" height="900"></canvas>

</div>

</div>


<script>

const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")

const n_slider = document.getElementById("n")
const drift_slider = document.getElementById("drift")
const iter_slider = document.getElementById("iter")
const radius_slider = document.getElementById("radius")

function updateLabels(){

document.getElementById("n_val").innerText = n_slider.value
document.getElementById("d_val").innerText = drift_slider.value
document.getElementById("i_val").innerText = iter_slider.value
document.getElementById("r_val").innerText = radius_slider.value

}

function draw(){

updateLabels()

let n = parseInt(n_slider.value)
let drift = parseFloat(drift_slider.value)
let iterations = parseInt(iter_slider.value)
let radius = parseFloat(radius_slider.value)

let base_angle = 2*Math.PI/n
let drift_rad = drift*Math.PI/180

ctx.clearRect(0,0,canvas.width,canvas.height)

ctx.save()

ctx.translate(canvas.width/2, canvas.height/2)

ctx.strokeStyle="#8fd"
ctx.lineWidth=1

ctx.beginPath()

for(let k=0;k<iterations;k++){

let theta = k*(base_angle + drift_rad)

let r = radius*(0.7 + 0.3*Math.cos(k*0.02))

let x = r*Math.cos(theta)*80
let y = r*Math.sin(theta)*80

if(k==0) ctx.moveTo(x,y)
else ctx.lineTo(x,y)

}

ctx.stroke()

ctx.restore()

}

function savePNG(){

let link = document.createElement("a")
link.download = "nexah_pattern.png"
link.href = canvas.toDataURL()
link.click()

}

n_slider.oninput = draw
drift_slider.oninput = draw
iter_slider.oninput = draw
radius_slider.oninput = draw

draw()

</script>

</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/" or self.path.startswith("/index"):

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(INDEX_HTML.encode())

        else:

            self.send_response(404)
            self.end_headers()


def run():

    print("NEXAH Pattern Explorer")
    print("Open browser: http://127.0.0.1:8000")

    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    run()

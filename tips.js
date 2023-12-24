forked from <a href="https://codepen.io/osublake/">Blake Bowen.</a>

<svg id="svg" viewBox="0 0 400 400">

  <defs>
    <circle class="handle" r="10" />
    <circle class="marker" r="4" />    
  </defs>
  
  <polygon id="star" points="261,220 298,335 200,264 102,335 139,220 42,149 162,148 200,34 238,148 358,149" />  
  <g id="marker-layer"></g>
  <g id="handle-layer"></g>
</svg>

body {
  background: #e8e9e8;
  font-family:sans-serif;
  color:#555;
}

#svg {
  position: fixed;
  top: 20px;
  left: 0;
  width: 100%;
  height: 100%;
}

#star {
  stroke: #29e;
  stroke-width: 20;
  stroke-linejoin: round;
  fill: none;
}

.handle {
  fill: #fff;
  fill-opacity: 0.4;
  stroke-width: 4;
  stroke: #fff;
}

.marker {
  fill: tomato;
  stroke: tomato;
  pointer-events: none;
}



a:link, a:visited, a:active {
  color:#555;
  text-decoration:none;
}

a:hover {
 
  color:#300;
}

//original by Blake Bowen https://codepen.io/osublake/
var star = document.querySelector("#star");
var markerDef = document.querySelector("defs .marker");
var handleDef = document.querySelector("defs .handle");
var markerLayer = document.querySelector("#marker-layer");
var handleLayer = document.querySelector("#handle-layer");

var points = [];
var numPoints = star.points.numberOfItems;

for (var i = 0; i < numPoints; i++) {  
  var point = star.points.getItem(i);
  points[i] = {x:point.x, y:point.y};
  createHandle(point);
}

function createHandle(point) {
    
  var marker = createClone(markerDef, markerLayer, point);
  var handle = createClone(handleDef, handleLayer, point);
  var update = function() { point.x = this.x; point.y = this.y; };
  
  var draggable = new Draggable(handle, {
    onDrag: update,
    onThrowUpdate: update,
    throwProps:true,
    liveSnap:{
      points:points,
      radius:15
    }
  });
}

function createClone(node, parent, point) {
  var element = node.cloneNode(true);
  parent.appendChild(element);
  TweenLite.set(element, { x: point.x, y: point.y });
  return element;
}


draggable="true" ondragstart="onDragStart(event)" ondragenter="onDragEnd(event)
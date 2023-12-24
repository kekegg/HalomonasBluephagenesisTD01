// renderer.js

var thrift = require('thrift');

var userService = require('./gen-nodejs/userService.js');
var {ttypes, mapOptions} = require('./gen-nodejs/tdmeta_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000, {
  transport: thrift.TBufferedTransport(),
  protocol: thrift.TBinaryProtocol()
  });
var thriftClient = thrift.createClient(userService,thriftConnection);



thriftConnection.on("error",function(e)
{
    console.log(e);
});

var ctx = document.getElementById("myChart");

//document.body.style.transform = 'scale(0.8)';

let expBtn = document.querySelector('#expBtn')
expBtn.addEventListener('click',() => {
  console.log("Draw svg map function!");
  mapOptions.zoomScale = 0.5;
  console.log(mapOptions.zoomScale)
  thriftClient.getMapData(mapOptions, (error, res) => {
    if(error) {
      console.error(error);
    } else {
      ctx.innerHTML = res;
      console.log(screen.width, screen.height)
      // window.scrollTo( 900, 1300 );
      // document.body.style.transform = 'translate(50%, 50%)';
    }
  })
 
})
expBtn.dispatchEvent(new Event('click'))


var rgtClickContextMenu = document.getElementById('bondMenu');

document.onclick = function(e) {
  // rgtClickContextMenu.style.display = 'none';
  // document.getElementById("rmenu").className = "hide"
  document.getElementById("bondMenu").className = "hide"
  // selectedAtoms = []
}

function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

function textClick(e, txt) {
  console.log(txt)
  thriftClient.drawSmiles(txt, (error, res) => {
    if(error) {
      console.error(error);
    } else {
      document.getElementById("bondMenu").className = "show";
      document.getElementById("bondMenu").style.top = mouseY(e) + 'px';
      document.getElementById("bondMenu").style.left =mouseX(e) + 'px';
      document.getElementById("showMeta").innerHTML = res;
    }
  }) 
}
// //deltaX, deltaY, offsetX, offsetY, clientX, clientY, 
// var startOffsetX = 0;
// var startOffsetY = 0;
// var startClientX = 0;
// var startOffsetY = 0;
//  function onDragStart(event) {
//   // store a ref. on the dragged elem
//   console.log("Drag start")
//   // dragged = event.target;
//   var a = document.getElementById("svgMap");
//   var svgDoc = a.contentDocument;
//   // var delta = svgDoc.getElementById("ps_rxn07433");
//   event.preventDefault(); 
//   // make it half transparent
//   // event.target.style.opacity = .5;
//   startOffsetX = event.offsetX;
//   startOffsetY = event.offsetY;
//   startClientX = event.clientX;
//   startClientY = event.clientY;
//   console.log(event.offsetX, event.clientX)
//   console.log(a.viewBox.animVal.width); //x, y, width, height
// };

// function onDragEnd(event) {
//   // reset the transparency
//   console.log("Draging")
//   var deltaX = event.offsetX - startOffsetX;
//   var deltaY = event.offsetY - startOffsetY;
//   a.viewBox.animVal.x = deltaX;
//   a.viewBox.animVal.y = deltaY;
//   console.log(deltaX, deltaY)
//   // event.target.style.opacity = "";
// };

var myChart = document.getElementById("svgMap");

function update() {
  console.log("Draggable")
	new Draggable(document.getElementById("myChart"), {
		bounds:myChart,
		edgeResistance:0.65,
		type:"x,y",
		throwProps:true,
    autoScroll:true,
    top:2300,
    left:1500,
	});
}

update();

function ZoomInput(event) {
  var zInput = document.getElementById("zoomRanger");
  console.log(zInput.value)
  mapOptions.zoomScale = zInput.value * 1.0 / 10.0;
  console.log(mapOptions.zoomScale)
  thriftClient.getMapData(mapOptions, (error, res) => {
    if(error) {
      console.error(error);
    } else {
      ctx.innerHTML = res;
      // console.log(screen.width, screen.height)
      // window.scrollTo( 900, 1300 );
      // document.body.style.transform = 'translate(50%, 50%)';
    }
  })
}

// var a = document.getElementById("svgMap");

// function createClone(node, parent, point) {
//   var element = node.cloneNode(true);
//   parent.appendChild(element);
//   TweenLite.set(element, { x: point.x, y: point.y });
//   return element;
// }
// function createHandle(a) {
    
//   // var marker = createClone(markerDef, markerLayer, point);
//   var handle = document.getElementById("result"); //createClone(handleDef, handleLayer, point);
//   var update = function() { a.viewBox.animVal.x = this.x; a.viewBox.animVal.y = this.y; 
//     console.log(a.viewBox.animVal.x, this.x)
//   };
  
//   var draggable = new Draggable(handle, {
//     onDrag: update,
//     onThrowUpdate: update,
//     throwProps:true,
//     // liveSnap:{
//     //   points:points,
//     //   radius:15
//     // }
//   });
// }
// createHandle(a);
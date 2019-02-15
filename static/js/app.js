var video = document.createElement("video");
var canvasElement = document.getElementById("canvas");
var canvas = canvasElement.getContext("2d");
var loadingMessage = document.getElementById("loadingMessage");
var outputContainer = document.getElementById("output");
var outputMessage = document.getElementById("outputMessage");
var outputData = document.getElementById("outputData");
var dietaryData = document.getElementById("dietary");
function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
}
// Use facingMode: environment to attemt to get the back camera on phones
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
    video.play();
    requestAnimationFrame(tick);
});
function tick() {
    loadingMessage.innerText = "⌛ Loading video..."
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      loadingMessage.hidden = true;
      canvasElement.hidden = false;
      outputContainer.hidden = false;
      canvasElement.height = video.videoHeight;
      canvasElement.width = video.videoWidth;
      canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
      var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
      var code = jsQR(imageData.data, imageData.width, imageData.height, {
        inversionAttempts: "dontInvert",
      });
      if (code) {
        drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
        drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
        drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
        drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
        outputMessage.hidden = true;
        outputData.parentElement.hidden = false;
        outputData.innerText = code.data;
        var task = "";
        if (document.getElementById('check-in').checked){
            task = "check-in";
        }
        else if (document.getElementById('sat-breakfast').checked){
            task = "sat-breakfast";
        }
        else if (document.getElementById('sat-lunch').checked){
            task = "sat-lunch";
        }
        else if (document.getElementById('sat-dinner').checked){
            task = "sat-dinner";
        }
        else if (document.getElementById('sun-breakfast').checked){
            task = "sun-breakfast";
        }
        else if (document.getElementById('sun-lunch').checked){
            task = "sun-lunch";
        }
        var url = "http://localhost:5000/req/" + task + "/" + code.data;
        $.get(url, function( data ) {
            if (!data.approved){
                outputData.innerText = "❌ " + data.error + " ❌";
                return;
            }
            var dietary_res = "";
            if (data.vegetarian){
                dietary_res += "🌿";
            }
            if (data.halal){
                dietary_res += "☪";
            }
            if (data.nut){
                dietary_res += "🥜";
            }
            if (data.vegan){
                dietary_res += "🌱";
            }
            outputData.innerText = "✅ " + data.name  + " completed task: " + task  + ". ✅";
            dietaryData.innerText = dietary;
        });
        setTimeout(function(){}, 1000);
      } else {
        outputMessage.hidden = false;
        outputData.parentElement.hidden = true;
      }
    }
    requestAnimationFrame(tick);
}

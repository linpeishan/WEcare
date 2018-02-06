//record local video
//start
var localVideoCapture = document.getElementById("localVideoCapture");
var localVideo = document.getElementById('localVideo');

var stream2;

//record
var mediaSource2 = new MediaSource();
mediaSource2.addEventListener('sourceopen', handleSourceOpen2, false);
var mediaRecorder2;
var recordedBlobs2;
var sourceBuffer2;

//--------------------------------------------------------------------

var recordButton2 = document.querySelector('button#record2');
var playButton2 = document.querySelector('button#play2');
var downloadButton2 = document.querySelector('button#download2');
recordButton2.onclick = toggleRecording2;
playButton2.onclick = play2;
downloadButton2.onclick = download2;
//-------------------------------------------------------------------
var stream2 = localVideo.captureStream(5);
console.log("stream start capturing...",stream2);


function handleSourceOpen2(event) {
  console.log('MediaSource2 opened');
  sourceBuffer2 = mediaSource2.addSourceBuffer('video/webm; codecs="vp8"');
  console.log('Source buffer: ', sourceBuffer2);
}

function handleDataAvailable2(event) {
  if (event.data && event.data.size > 0) {
    recordedBlobs2.push(event.data);
  }
}

function handleStop2(event) {
  console.log('Recorder stopped: ', event);
}

function toggleRecording2() {
  if (recordButton2.textContent === 'Start User Recording') {
    startRecording2();
  } else {
    stopRecording2();
    recordButton2.textContent = 'Start User Recording';
    playButton2.disabled = false;
    downloadButton2.disabled = false;
  }
}

function startRecording2() {
  var options = {mimeType: 'video/webm'};
  recordedBlobs2 = [];
  try {
    mediaRecorder2 = new MediaRecorder(stream2, options);
  } catch (e0) {
    console.log('Unable to create MediaRecorder2 with options Object: ', e0);
    try {
      options = {mimeType: 'video/webm,codecs=vp9'};
      mediaRecorder2 = new MediaRecorder(stream2, options);
    } catch (e1) {
      console.log('Unable to create MediaRecorder with options Object: ', e1);
      try {
        options = 'video/vp8'; // Chrome 47loca
        mediaRecorder2 = new MediaRecorder(stream2, options);
      } catch (e2) {
        alert('MediaRecorder2 is not supported by this browser.\n\n' +
            'Try Firefox 29 or later, or Chrome 47 or later, with Enable experimental Web Platform features enabled from chrome://flags.');
        console.error('Exception while creating MediaRecorder2:', e2);
        return;
      }
    }
  }
  console.log('Created MediaRecorder', mediaRecorder2, 'with options', options);
  recordButton2.textContent = 'Stop User Recording';
  playButton2.disabled = true;
  downloadButton2.disabled = true;
  mediaRecorder2.onstop = handleStop2;
  mediaRecorder2.ondataavailable = handleDataAvailable2;
  mediaRecorder2.start(100); // collect 100ms of data
  console.log('MediaRecorder started', mediaRecorder2);
}

 function stopRecording2() {
  mediaRecorder2.stop();
  console.log('Recorded Blobs: ', recordedBlobs2);
  localVideoCapture.controls = true;
}

function play2() {
  var superBuffer2 = new Blob(recordedBlobs2, {type: 'video/webm'});
  localVideoCapture.src = window.URL.createObjectURL(superBuffer2);
}

function download2() {
  var blob = new Blob(recordedBlobs2, {type: 'video/webm'});
  var url = window.URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = 'usersvideo.webm';
  document.body.appendChild(a);
  a.click();
  setTimeout(function() {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 100);
}













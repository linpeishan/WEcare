//Create an account on Firebase, and use the credentials they give you in place of the following
// Initialize Firebase
var config = {
apiKey: "AIzaSyCscKJK9lsw_dAV1ExufKIhvPtMSZNxig0",
authDomain: "hello-b0bf7.firebaseapp.com",
databaseURL: "https://hello-b0bf7.firebaseio.com",
projectId: "hello-b0bf7",
storageBucket: "hello-b0bf7.appspot.com",
messagingSenderId: "776232646563"
};
firebase.initializeApp(config);


// var hangupButton = document.getElementById('hangUp');
// hangupButton.disabled = true;


var database = firebase.database().ref();
var localVideo = document.getElementById("localVideo");
var remoteVideo = document.getElementById("remoteVideo");
var yourId = Math.floor(Math.random()*1000000000);
var servers = {'iceServers': [{'urls': 'stun:stun.services.mozilla.com'}, {'urls': 'stun:stun.l.google.com:19302'}, {'urls': 'turn: numb.viagenie.ca','credential': 'Peishan Lin','username': 'psnilx@gmail.com'}]};
var pc = new RTCPeerConnection(servers);
pc.onicecandidate = (event => event.candidate?sendMessage(yourId, JSON.stringify({'ice': event.candidate})):console.log("Sent All Ice") );
pc.onaddstream = (event => remoteVideo.srcObject = event.stream);

function sendMessage(senderId, data) {
    var msg = database.push({ sender: senderId, message: data });
    msg.remove();
}

function readMessage(data) {
    var msg = JSON.parse(data.val().message);
    var sender = data.val().sender;
    if (sender != yourId) {
        if (msg.ice != undefined)
            pc.addIceCandidate(new RTCIceCandidate(msg.ice));
        else if (msg.sdp.type == "offer")
            pc.setRemoteDescription(new RTCSessionDescription(msg.sdp))
              .then(() => pc.createAnswer())
              .then(answer => pc.setLocalDescription(answer))
              .then(() => sendMessage(yourId, JSON.stringify({'sdp': pc.localDescription})));
        else if (msg.sdp.type == "answer")
            pc.setRemoteDescription(new RTCSessionDescription(msg.sdp));
    }
};

database.on('child_added', readMessage);

function showLocalVideo() {
  navigator.mediaDevices.getUserMedia({audio:true, video:true})
    .then(stream => localVideo.srcObject = stream)
    .then(stream => pc.addStream(stream))
    .catch(function(err) {
       console.log(err);
    });
}

function showRemoteVideo() {
  pc.createOffer()
    .then(offer => pc.setLocalDescription(offer) )
    .then(() => sendMessage(yourId, JSON.stringify({'sdp': pc.localDescription})) );
}

var videoElement = document.getElementById("remoteVideo");

  function toggleFullScreen() {
    if (!document.mozFullScreen && !document.webkitFullScreen) {
      if (videoElement.mozRequestFullScreen) {
        videoElement.mozRequestFullScreen();
      } else {
        videoElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
      }
    } else {
      if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else {
        document.webkitCancelFullScreen();
      }
    }
  }

  document.addEventListener("keydown", function(e) {
    if (e.keyCode == 13) {
      toggleFullScreen();
    }
  }, false);


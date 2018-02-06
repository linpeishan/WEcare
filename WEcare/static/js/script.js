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
// SEND DATA: OFFER, ANSWER AND ICE Candidate Objects

var database = firebase.database().ref(); //read data when the message is inserted.
var localVideo = document.getElementById("localVideo");
var remoteVideo = document.getElementById("remoteVideo");
var yourId = Math.floor(Math.random()*1000000000);
//ICE Candidate START----------
var servers = {'iceServers': [{'urls': 'stun:stun.services.mozilla.com'},
{'urls': 'stun:stun.l.google.com:19302'},
{'urls': 'turn: numb.viagenie.ca','credential': 'Peishan Lin','username': 'psnilx@gmail.com'}]};
//Peer Connection
var pc = new RTCPeerConnection(servers); // creates a PeerConnection oject on your computer
pc.onicecandidate = (event => event.candidate?sendMessage(yourId, JSON.stringify({'ice': event.candidate})):console.log("Sent All Ice") );
//waits for an ICE Candidate object to be created on your computer.
pc.onaddstream = (event => remoteVideo.srcObject = event.stream);
// ICE Candidate END ----
function sendMessage(senderId, data) {
    var msg = database.push({ sender: senderId, message: data });
    msg.remove();
}

function readMessage(data) {
    var msg = JSON.parse(data.val().message); // convert string back to ICE Candidate obj
    var sender = data.val().sender;
    if (sender != yourId) { //check if the sender has the same ID as you,ignores it if it's the same(thatt's you)
        if (msg.ice != undefined)
            pc.addIceCandidate(new RTCIceCandidate(msg.ice));
        else if (msg.sdp.type == "offer")
            pc.setRemoteDescription(new RTCSessionDescription(msg.sdp)) // send Remote description to the Offer Object that you sent
              .then(() => pc.createAnswer()) //create ans obj
              .then(answer => pc.setLocalDescription(answer)) //setLocalDescription: several ICE Candidate will be created
              .then(() => sendMessage(yourId, JSON.stringify({'sdp': pc.localDescription})));
        else if (msg.sdp.type == "answer")
            pc.setRemoteDescription(new RTCSessionDescription(msg.sdp)); //read msg
    }
}; //Offer object in JSON

database.on('child_added', readMessage);

function showLocalVideo() {
  navigator.mediaDevices.getUserMedia({audio:true, video:true}) //getUserMedia: ask to access the camera
    .then(stream => localVideo.srcObject = stream)
    .then(stream => pc.addStream(stream))
    .catch(function(err) {
       console.log(err);
    });
}

function showRemoteVideo() {
//ICE Candidate START ---
  pc.createOffer() //return an Offer Obj
    .then(offer => pc.setLocalDescription(offer) )
//ICE Candidate END ---
    .then(() => sendMessage(yourId, JSON.stringify({'sdp': pc.localDescription})) ); //send that Offer object to your friend
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
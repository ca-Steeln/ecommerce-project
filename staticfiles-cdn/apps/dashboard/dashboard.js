
console.log('djaja');
const socket = new WebSocket(`ws://${window.location.host}/ws/dashboard/`);
console.log(socket);

socket.onmessage = function(e) {
    console.log(`Server: ${e.data}`);
}

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'message': 'Hello Dashboard',
        'sender': 'dashboard',
        })
    );
}
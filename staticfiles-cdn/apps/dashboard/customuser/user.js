

const userPK = document.getElementById('obj-pk').textContent.trim();
const socket = new WebSocket(`ws://${window.location.host}/ws/dashboard/users/${userPK}/`);
console.log(socket);

socket.onmessage = function(e) {
    console.log(`Server: ${e.data}`);
    const {sender, message} = JSON.parse(e.data)

    console.log(sender)
}

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'message': 'Hello User',
        'sender': 'CustomUser',
        })
    );
}
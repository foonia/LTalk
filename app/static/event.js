function init() {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    const editor = document.querySelector('#editor + .CodeMirror');
    editor.addEventListener("keypress", event => {
        if (event.isComposing || event.keyCode === 229) {
            return;
        }
        console.log(event.KeyCode)
        socket.emit('key_press', {
            keyCode: "{{event.keyCode}}"
        });
    });
}

/*
socket.on('connect',function(){
    socket.emit('join_room',{
        username : "{{ username }}",
        room : "{{ room }}"
    })
});

socket.on('join_room_announcement', function(data){
    console.log(data);
    const newNode = document.createElement('div');
    newNode.innerHTML = '<b>' + data.username + '</b>' + ' : has joined the room';
    document.getElementById('messages').appendChild(newNode);
});
*/

init();
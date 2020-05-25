function init() {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    const editor = document.querySelector('#editor + .CodeMirror');

    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('join_room_announcement', data => {
        console.log(data);
    });

    socket.on('message', data => {
        console.log(data);
    });

    editor.addEventListener("keypress", event => {
        if (event.isComposing || event.keyCode === 229) {
            return;
        }

        console.log(event.keyCode);
        socket.emit('key_press', {keyCode: event.keyCode});
    });
}


init();
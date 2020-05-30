/*
* 먼저, doc에 콜백 형식으로 on을 붙이면 doc가 리턴이 안되는 문제는 왜 발생하는지
* 그리고, addEventListener과 on의 차이점이 뭔지 모르겠다..
* */

function init() {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function () {
        socket.emit('joined', {});
    });

    const doc = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: "javascript",
        lineNumbers: true,
    });
    doc.on('change', (CodeMirror, object) => {
        console.log(object);
        socket.emit('key_press', JSON.stringify(object));
    });

    const editor = document.querySelector('#editor + .CodeMirror');


    // 입력으로 받은 room에 접속 시, connect되고 서버에서 같은 room에 있는 클라이언트들에게 호출되는 함수
    socket.on('join_room_announcement', data => {
        console.log('in ' + data['room']);
    });

    // 서버로 부터 받은 데이터, chageobj 객체로 변환하여 변경하상 적용해줌.
    socket.on('message', data => {
        let changeObj = JSON.parse(data);
        if(changeObj.origin === "+input") {
            doc.replaceRange(changeObj.text[0], changeObj.to);
        }
        else if(changeObj.origin === "+delete") {

        }
    });
}


init();
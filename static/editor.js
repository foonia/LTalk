function init() {
    let editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: "javascript",
        lineNumbers: true,
    });
    editor.save()
}

init();
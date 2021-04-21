function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

$(document).ready(function() {
    namespace = '/global';

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('log', function(msg) {
        $('#log').append('<br>' + $('<div/>').text('Received ' + msg.type + ': ' + msg.data).html());
    });

    socket.on('heartbeat', function(msg) {
        heatbeat_time = Date(msg.datetime)
        $('#heartbeat').text('Received #' + msg.count + ': ' + heatbeat_time);
    });

    socket.on('update', function(msg) {
        console.log(msg)
        row = $("#"+msg["uuid"]).find(".status").html(`<td class="status">${msg["status"]}</td>`)
        if (msg["error"]) {
            row = $("#"+msg["uuid"]).find(".download").html(`<td class="download">N/A - Error!</td>`)
        }
        else {
            row = $("#"+msg["uuid"]).find(".download").html(`<td class="download"><a href="${msg["url"]}">Download</a></td>`)
        }
    });


    // Send updates
    $('#submit').click(function(event) {
        uuid = uuidv4()
        filename = $("#filename").val()
        text = $('#text').val()
        datetime = Date()
        ssml = $('#ssml').is(":checked")
        payload = {"uuid": uuid, "filename": filename, "text": text, "datetime": datetime, "ssml": ssml}
        socket.emit('update', payload)
        $('#log').prepend(`
            <tr id=${uuid}>
                <td class="uuid">${uuid}</td>
                <td class= "filename">${filename}</td>
                <td class="timestamp">${datetime}</td>
                <td class="status">Pending</td>
                <td class="download">Pending</td>
            </tr>
            `);
    });
});
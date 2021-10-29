$(document).ready(function() {
    try {
        let re = new RegExp($("#text_input").val(), 'gim')
        $(".text_output").markRegExp(re);
    } catch (error) {
        //console.error(error)
    }

    $('.playback_rate').change(function(event) {
        $('.playback_rate').val(this.value)
        var players = $('.audio_player')

        for (let i = 0; i < players.length; i++) {
            players[i].playbackRate = this.value
        }
    });
});
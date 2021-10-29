$(function() {
    $('input[name="date_filter"]').daterangepicker({
        timePicker: true,
        autoUpdateInput: false,
        locale: {
            cancelLabel: 'Clear',
            format: 'MM/DD/YYYY hh:mm A'
        }
    });

    $('input[name="date_filter"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY hh:mm A') + ' - ' + picker.endDate.format('MM/DD/YYYY hh:mm A'));
    });

    $('input[name="date_filter"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

});

$(document).ready(function() {
    try {
            let re = new RegExp($("#text_input").val(), 'gim')
    $(".text_output").markRegExp(re);
    } catch (error) {
        console.error(error)
    }

});
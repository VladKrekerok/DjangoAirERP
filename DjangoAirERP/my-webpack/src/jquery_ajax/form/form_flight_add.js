$(function ($) {
    $('#form_flight').submit(function (e) {
        e.preventDefault()
        console.log(this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log(response)
                document.location.href = "/management/flights";
            },
            error: function (response) {
                console.log(response)
                if (response.status === 400) {
                    $('#flight_alert').text(response.responseJSON['error']).removeAttr('style')
                }
            }
        })
    })
})

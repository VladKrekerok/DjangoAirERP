$(function ($) {
    $('#my_login').submit(function (e) {
        e.preventDefault()
        console.log(this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log(response)
                window.location.reload();
            },
            error: function (response) {
                console.log(response)
                if (response.status === 400) {
                    $('#login_alert').text(response.responseJSON['error']).removeAttr('style')
                }
            }
        })
    })
})

$(function ($) {
    $('#tickets_reg').submit(function (e) {
        e.preventDefault()
        console.log(this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log(response)
                document.location.href = response.url;
            },
            error: function (response) {
                console.log(response)
                if (response.status === 401) {
                    $('#tickets_alert').text(response.responseJSON['error']).removeAttr('style')
                }
            }
        })
    })
})

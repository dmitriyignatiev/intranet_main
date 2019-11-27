
$(document).ready(function(){
    $('#form_invoice').on('submit', function(e) {
            e.preventDefault();
            var fin_d = $('#fin_id').text()
    
    
            var formData = new FormData($(this)[0]);
            var msg_error = 'An error has occured. Please try again later.';
            var msg_timeout = 'The server is not responding';
            var message = '';
            var form = $('#form_invoice');
            $.ajax({

    
                data: formData,
                find:fin_d,
                async: false,
                // cache: false,
                processData: false,
                contentType: false,
                url: form.attr('action'),
                type: form.attr('method'),
    
                error: function(xhr, status, error) {
                    if (status === "timeout") {
                        alert(msg_timeout);
                    } else {
                        alert(msg_error);
                    }
                },
                success: function(response) {
                    $('#successAlert').text(response.success).show();
                    $('#errorAlert').hide();
    
                },
                timeout: 7000
            });
        });


       
});

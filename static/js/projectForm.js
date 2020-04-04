(function ($) {
    'use strict';

    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                if (form.checkValidity() === false) {
                    event.stopPropagation();
                } else {
                    var f = $(this);
                    var url = "/api/post/project"

                    $.ajax({
                        type: "POST",
                        url: url,
                        data: f.serialize(), // serializes the form's elements.
                        success: function(data)
                        {
                            console.log(data)
                            if (data.redirectUrl != undefined){
                                window.location.replace(data.redirectUrl);
                            } else {
                                // display the error
                            }

                        }
                    });
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);


})(jQuery);

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
                    var url = "/api/epicIssuesFullDetails/" + $('#repoId').val() + "/" + $('#epicId').val()

                    $.ajax({
                        type: "GET",
                        url: url,
                        success: function(epicsIssuesDataResponse)
                        {
                            var tableRow = '<p>The following issues were fetched, does this look correct to you?</p><table class="table table-sm table-hover"><thead><tr><th scope="col">Issue #</th><th scope="col">Description</th></tr></thead><tbody>'
                            if (epicsIssuesDataResponse.epicsIssues.length == 0){
                                // display the error
                                tableRow += '<tr><th scope="row">0</th><td>Unfortunately there are no issues assigned to this epic</td></tr>'
                            } else {
                                console.log(epicsIssuesDataResponse)

                                 $.each(epicsIssuesDataResponse.epicsIssues, function(key, epicsIssue) {
                                    console.log(key)
                                    console.log(epicsIssue)
                                    tableRow += '<tr><th scope="row">'+epicsIssue.issueNumber+'</th><td>'+ epicsIssue.title+'</td></tr>'
                                 });
                            }
                            tableRow += '</tbody></table><button class="btn btn-primary" type="submit" id="add_all_issues" value="'+$('#epicId').val()+'">Add All Issues</button>'

                            $('#fetchedEpicData').html(tableRow)
// Make the modal appear
                        }
                    });
                }

                form.classList.add('was-validated');
            }, false);
        });
    }, false);

// TODO: put tableRow in a modal
// TODO: make a call with POST on button add_all_issues press

})(jQuery);

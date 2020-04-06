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
                    var url = "/api/epicIssuesFullDetails/" + $('#boardName').val() + "/" + $('#epicId').val()

                    $.ajax({
                        type: "GET",
                        url: url,
                        success: function(epicsIssuesDataResponse)
                        {
                            $('#addIssueButton').show()
                            $('#epicsModalLabel').text($( "#epicId option:selected" ).text());
                            var tableRow = '<p>The following issues were fetched, does this look correct to you?</p><table class="table table-sm table-hover"><thead><tr><th scope="col">Issue #</th><th scope="col">Description</th></tr></thead><tbody>'
                            if (epicsIssuesDataResponse.epicsIssues.length == 0){
                                // display the error
                                tableRow += '<tr><th scope="row">0</th><td>Unfortunately there are no issues assigned to this epic</td></tr>'
                                tableRow += '</tbody></table>'
                                $('#addIssueButton').hide()
                            } else {
                                console.log(epicsIssuesDataResponse)

                                 $.each(epicsIssuesDataResponse.epicsIssues, function(key, epicsIssue) {
                                    tableRow += '<tr><th scope="row">'+epicsIssue.issueNumber+'</th><td>'+ epicsIssue.title+'</td></tr>'
                                 });
                                 tableRow += '</tbody></table>'
                                 $('#addIssueButton').val($('#epicId').val())
                            }


                            $('#fetchedEpicData').html(tableRow)
                            $('#hiddenFetchButton').click()
                        }
                    });
                }

                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    $('#addIssueButton').click(function(){
        var epicId = $('#addIssueButton').val()
        var projectId = $('#projectId').val()
        var url = "/api/post/projectEpicsAndTickets"

        console.log(epicId)
        $.ajax({
            type: "POST",
            data: {'projectId': projectId, 'type': 'epic', 'id': epicId},
            url: url,
            success: function(peatResponse)
            {
                console.log(peatResponse)
                if (peatResponse.redirectUrl != undefined){
                    window.location.replace(peatResponse.redirectUrl);
                } else {
                    // TODO: display the error on the modal
                }
            }
        });
    })

    $("#searchInputField").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".table tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });

})(jQuery);

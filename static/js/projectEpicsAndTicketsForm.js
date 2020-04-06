(function ($) {
    'use strict';

    window.addEventListener('load', function() {

        var forms = $('#projectEpicsForm');
        var epicForm = $('#projectEpicsForm');
        var epicValidation = Array.prototype.filter.call(epicForm, function(formResponse) {
            fetch_epic_modal(formResponse)
        });

        var issueForm = $('#projectIssueForm');
        var issueValidation = Array.prototype.filter.call(issueForm, function(formResponse) {
            fetch_epic_modal(formResponse)
        });

    }, false);


    function fetch_epic_modal(form){

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (form.checkValidity() === false) {
                event.stopPropagation();
            } else {
                var thisForm = $(this)
                var idType = thisForm.find('input[name="type"]').val()
                var id = thisForm.find('input[name="id"]').val()
                var url = "/api/github/issue/" + $('#boardName').val() + "/" + id
                if(idType == "epic"){
                    id = thisForm.find('select[name="id"]').val()
                    url = "/api/epicIssuesFullDetails/" + $('#boardName').val() + "/" + id
                }


                $.ajax({
                    type: "GET",
                    url: url,
                    success: function(epicsIssuesDataResponse)
                    {
                        $('#addIssueButton').show()
                        if(idType == "epic"){
                            $('#dataType').val('epic')
                            $('#epicsModalLabel').text($( "#id option:selected" ).text());
                        } else {
                            $('#dataType').val('issue')
                            $('#epicsModalLabel').text("Confirm issue");
                        }
                        var tableRow = '<div id="errorMessage"></div><p>The following issues were fetched, does this look correct to you?</p><table class="table table-sm table-hover"><thead><tr><th scope="col">Issue #</th><th scope="col">Description</th></tr></thead><tbody>'

                        if(idType == "epic"){
                            var issue = epicsIssuesDataResponse.epicsIssues
                            var message = "Unfortunately there are no issues assigned to this epic"

                        } else {
                            // issue
                            var issue = epicsIssuesDataResponse.issues
                            var message = "Unfortunately, this issue was not found on Github"
                        }


                        if (issue.length == 0){
                            // display the error
                            tableRow += '<tr><th scope="row">0</th><td>' + message + '</td></tr>'
                            tableRow += '</tbody></table>'
                            $('#addIssueButton').hide()
                        } else {
                            console.log(epicsIssuesDataResponse)

                             $.each(issue, function(key, epicsIssue) {
                                tableRow += '<tr><th scope="row">'+epicsIssue.issueNumber+'</th><td>'+ epicsIssue.title+'</td></tr>'
                             });
                             tableRow += '</tbody></table>'
                             if(idType == "epic"){
                                $('#addIssueButton').val($('#id').val())
                            } else {
                                $('#addIssueButton').val(issue[0].issueNumber)
                            }
                        }

                        $('#fetchedEpicData').html(tableRow)
                        $('#hiddenFetchButton').click()
                    }
                });
            }

            form.classList.add('was-validated');
        }, false);


    }

    $('#addIssueButton').click(function(){
        var epicId = $('#addIssueButton').val()
        var projectId = $('#projectId').val()
        var url = "/api/post/projectEpicsAndTickets"

        console.log(epicId)
        $.ajax({
            type: "POST",
            data: {'projectId': projectId, 'type': $('#dataType').val(), 'id': epicId},
            url: url,
            success: function(peatResponse)
            {
                console.log(peatResponse)
                if (peatResponse.redirectUrl != undefined){
                    window.location.replace(peatResponse.redirectUrl);
                } else if (peatResponse.message != undefined) {
                    $('#errorMessage').html('<div class="alert alert-danger">'+peatResponse.message+'</div>')
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

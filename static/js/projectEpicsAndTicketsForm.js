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


    $('#updateTicketModal').on('shown.bs.modal', function(e){
        console.log("openned!")
        var ticketId = $(e.relatedTarget).data('ticketid');
        var issueNumber = $(e.relatedTarget).data('issuenumber');
        var title = $(e.relatedTarget).data('title');
        var dependantSystem = $(e.relatedTarget).data('dependantsystem');
        var dependantReason = $(e.relatedTarget).data('dependantreason');
        var devEstimateInDays = $(e.relatedTarget).data('devestimateindays');
        var qaEstimateInDays = $(e.relatedTarget).data('qaestimateindays');
        var issueStatus = $(e.relatedTarget).data('issuestatus');
        var proposedReleaseDropTo = $(e.relatedTarget).data('proposedreleasedropto');
        var totalComments = $(e.relatedTarget).data('totalcomments');
        var notes = $(e.relatedTarget).data('notes');
        var sharedPlatformIssue = $(e.relatedTarget).data('sharedplatformissue');

        $('#updateTicketModalLabel').text()

        var form=`
        <div class="modal-header">
            <h5 class="modal-title" id="updateTicketModalLabel">${issueNumber}: ${title}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <form class="form-horizontal" id="ticketForm" method="post" action="/api/post/ticket/${$('#boardName').val()}/${issueNumber}">
            <div class="modal-body text-left">
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Dependant system</span>
                        </div>
                        <input type="text" value="${dependantSystem}" class="form-control" autocomplete="off" name="dependantSystem" placeholder="Dependant system">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Dependant reason</span>
                        </div>
                        <input type="text" value="${dependantReason}" class="form-control" autocomplete="off" name="dependantReason" placeholder="Dependant reason">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Developer estimate in days</span>
                        </div>
                        <input type="text" value="${devEstimateInDays}" class="form-control" autocomplete="off" name="devEstimateInDays" placeholder="Developer estimate in days">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">QA estimate in days</span>
                        </div>
                        <input type="text" value="${qaEstimateInDays}" class="form-control" autocomplete="off" name="qaEstimateInDays" placeholder="QA estimate in days">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Scope / proposed released to version</span>
                        </div>
                        <input type="text" value="${proposedReleaseDropTo}" class="form-control" autocomplete="off" name="proposedReleaseDropTo" placeholder="Scope / proposed released to version">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Notes</span>
                        </div>
                        <input type="text" value="${notes}" class="form-control" autocomplete="off" name="notes" placeholder="Notes">
                    </div>
                </div>
                <div class="row">
                    <div class="input-group col-sm-12">
                        <div class="input-group-prepend">
                            <span class="input-group-text">Shared platform issue?</span>
                        </div>
                        <input type="text" value="${sharedPlatformIssue}" class="form-control" autocomplete="off" name="sharedPlatformIssue" placeholder="Shared platform issue?">
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <input type="hidden" name="projectId" value="${$('#projectId').val()}">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                <button class="btn btn-primary" type="submit">Update</button>
            </div>
        </form>
        `;

        // update ticket
        $('#fetchedUpdateTicket').html(form);
    });
})(jQuery);

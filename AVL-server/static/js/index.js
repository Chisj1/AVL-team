API = "http://127.0.0.1:8080/api/check"

$("#url_form").submit(function(e) {
    e.preventDefault();
})

$("#submit_url").click(function() {
    let url = $("#check_url").val();
    $.get(API, { url: url }, function(data) {
        if (data == 1) {
            $("#result").html('<div class="result unsafe">This is a phishing URL</div>')
        } else {
            $("#result").html('<div class="result safe">This is a safe URL</div>')
        }
    })
})

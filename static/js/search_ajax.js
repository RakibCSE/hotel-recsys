$(function () {
    $("#place").keyup(function () {
        $.ajax({
            type: "GET",
            url: "/search_ajax",
            data: {
                'place_text': $("#place").val(),
            },
            success: function (response) {
                let response_data = JSON.parse(response);

                // Empty the result box first
                $("#result").empty();

                for (const key in response_data) {
                    if (key == "status") {
                        $("#result").empty();
                    } else if (response_data.hasOwnProperty(key)) {
                        const element = response_data[key];

                        let html = `
                                    <li>
                                        <div class="collapsible-header">
                                            <i class="material-icons prefix">place</i>
                                            <strong>${element["heading"]}</strong>
                                        </div>
                                        <div class="collapsible-body">
                                            <div class="collection" id="${key}">
                                            </div>
                                        </div>
                                    </li>
                                    `

                        console.log(key, element["heading"]);
                        $("#result").append(html);

                        element["result"].forEach(country => {
                            if (country != "nan") {
                                $(`#${key}`).append(`<a class="collection-item" style="color: black;">${country}</a>`);
                            }
                        });
                    }
                }
            }
        });
    });
});
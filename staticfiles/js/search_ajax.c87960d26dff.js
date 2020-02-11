$(function () {
    $("#place").keyup(function () {
        $.ajax({
            type: "GET",
            url: "/search/",
            data: {
                'place_text': $("#place").val(),
            },
            success: function (response) {
                let search_response = JSON.parse(response);

                let search_dict = {};
                for (let i = 0; i < search_response.length; i++) {
                    search_dict[search_response[i][0]] = search_dict[search_response[i][1]];
                }
                console.log(search_response);
                $('input.autocomplete').autocomplete({
                    data: search_response,
                    limit: 5, // The max amount of results that can be shown at once. Default: Infinity.
                });
            }

        });
    });
});

// function searchSuccess(hotel_data) {
//     $("#place-results").html(hotel_data);
// }

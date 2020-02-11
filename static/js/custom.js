function hide_reveal() {
    let x = document.getElementById("search-box");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

$("#search-box").ready(function () {
    let x = document.getElementById("search-box");
    x.style.display = "none";
});

$("#alert_close").click(function () {
    $("#alert_box").fadeOut("slow");
});

$(document).ready(function () {
    $('.sidenav').sidenav();

    $('.datepicker').datepicker({
        format: "dd-mm-yyyy"
    });

    $('.parallax').parallax();
    $('.slider').slider();
    $('.collapsible').collapsible();
});

$('.head-link').click(function (e) {
    e.preventDefault();

    let goto = $(this).attr('href');

    $('html, body').animate({
        scrollTop: $(goto).offset().top
    }, 800);
});
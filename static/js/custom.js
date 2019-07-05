$(document).ready(function () {
    $('.sidenav').sidenav();

    $('.datepicker').datepicker({
        format: "dd-mm-yyyy"
    });
});

$(document).ready(function () {
    $('.parallax').parallax();
});

$(document).ready(function () {
    $('.slider').slider();
});

$('.head-link').click(function (e) {
    e.preventDefault();

    let goto = $(this).attr('href');

    $('html, body').animate({
        scrollTop: $(goto).offset().top
    }, 800);
});
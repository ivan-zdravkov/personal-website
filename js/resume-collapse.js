function expand() {
    var container = $('.resume-container');
    var down = $('.resume-collapser .down');
    var up = $('.resume-collapser .up');

    container.addClass('expanded');
    down.addClass('d-none');
    up.removeClass('d-none');
}

function collapse() {
    var container = $('.resume-container');
    var down = $('.resume-collapser .down');
    var up = $('.resume-collapser .up');

    container.removeClass('expanded');
    down.removeClass('d-none');
    up.addClass('d-none');

    $('html, body').animate({
        scrollTop: container.offset().top
    }, 1000);
}
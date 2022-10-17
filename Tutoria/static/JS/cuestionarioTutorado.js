$(document).ready(function () {
    // executes when HTML-Document is loaded and DOM is ready
    console.log("document is ready");


    $(".col-md-8").hover(
        function () {
            $(this).addClass('shadow-lg');
        }, function () {
            $(this).removeClass('shadow-lg');
        }
    );

    // document ready  
});
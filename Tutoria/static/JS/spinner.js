$(document).ready(function () {

    $("#formIntegrar").submit(function () {
        //console.log("entrando al spinner.....");
        var btn = $("#boton1");
        var html = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Cargando..";
        btn.html(html);
    });

    $("#formCredito").submit(function () {
        var btn = $("#boton2");
        var html = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Cargando..";
        btn.html(html);
    });


});

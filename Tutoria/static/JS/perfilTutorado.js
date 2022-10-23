$(document).ready(function () {
  $("#User_first_name").val(
    $("#User_first_name").val() + " " + $("#User_last_name").val()
  );
  if ($("#PadreMadreTutor_nombre").val() != "") {
    $("#PadreMadreTutor_nombre").val(
      $("#PadreMadreTutor_nombre").val() +
        " " +
        $("#PadreMadreTutor_apellidos").val()
    );
  }
});

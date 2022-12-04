$(document).ready(function () {
  $(".datatable").DataTable({
    responsive: true,
    lengthChange: false,
    autoWidth: false,
    dom: "Bfrtip",
    lengthMenu: [
      [5, 10, 25, 50, -1],
      ["5 filas", "10 filas", "25 filas", "50 filas", "Show filas"],
    ],
    buttons: ["pageLength", "copy", "csv", "excel", "pdf", "print"],
    language: {
      url: "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
    },
    ordering: true,
  });
});

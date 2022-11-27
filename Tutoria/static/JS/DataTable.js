$(document).ready(function () {
  $(".datatable").DataTable({
    responsive: true,
    lengthChange: false,
    autoWidth: false,
    dom: "Bfrtip",
    lengthMenu: [
      [3, 5, 10, 25, 50, -1],
      ["3 rows", "5 rows", "10 rows", "25 rows", "50 rows", "Show all"],
    ],
    buttons: ["pageLength", "copy", "csv", "excel", "pdf", "print"],
    language: {
      url: "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
    },
    ordering: true,
  });
});

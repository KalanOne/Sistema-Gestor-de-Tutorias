$(document).ready(function () {
  $("#liveToastBtn").click(function () {
    let toastHTML = document.getElementById("liveToast");
    let toastElement = new bootstrap.Toast(toastHTML);
    toastElement.show();
  });
});

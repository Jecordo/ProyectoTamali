$(document).ready(function () {
  $("#searchInput").on("input", function () {
    var searchText = $(this).val().toLowerCase();
    $("tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(searchText) > -1);
    });
  });
});

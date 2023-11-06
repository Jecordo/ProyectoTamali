$(document).ready(function () {
  $("#cod_producto_id").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });
});

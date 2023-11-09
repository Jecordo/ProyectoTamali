$(document).ready(function () {
  $("#cod_producto_id").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });

  $("#marca_producto").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
    width: 'resolve'
  });

  $("#categoria_producto").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });

  $("#prov_producto").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });
});

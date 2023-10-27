$(document).ready(function () {
  var input1Elements = document.querySelectorAll(".cantidad");
  var input2Elements = document.querySelectorAll(".total_producto");
  var input3Elements = document.querySelectorAll(".precio_unit");

  input1Elements.forEach(function (input1, index) {
    input1.addEventListener("input", function () {
      // Obtén el valor del input1 que se está modificando
      var value = this.value;
      var precio = input3Elements[index].value;

      // Obtén el input2 correspondiente
      var input2 = input2Elements[index];

      // Actualiza el valor de input2
      input2.value = value * precio;
    });
  });

  $("#cod_producto_id").select2({
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });

  // Deshabilita todos los enlaces
  $(window).on("beforeunload", function () {
    if (facturaIncompleta) {
      return "Debe finalizar la facturación antes de salir de esta página.";
    }
  });

  $("#finalizar_factura").click(function () {
    facturaIncompleta = false;
  });

  $("a").attr("disabled", true).addClass("disabled");

  $("button").attr("disabled", true);

  $("#anhadir_producto").attr("disabled", false);
  $("#id_detalle").attr("disabled", false);
  $("#finalizar_factura").attr("disabled", false).removeClass("disabled");
  $("#cancelar_factura").attr("disabled", false).removeClass("disabled");
});

$(document).ready(function () {
  var cantidades_productos = document.querySelectorAll(".cantidad");
  var total_precio_producto = document.querySelectorAll(".total_producto");
  var precios_unitarios = document.querySelectorAll(".precio_unit");
  var iva_productos = document.querySelectorAll(".iva");
  var descuentos = document.querySelectorAll(".descuento_prodcuto");
  var total_iva = document.getElementById("total_iva");
  var total_compra = document.getElementById("total_productos");
  var formu_eliminar = document.querySelectorAll(".delete_button");

  cantidades_productos.forEach(function (input, index) {
    input.addEventListener("input", function () {
      actualizarValores(index);

      const iva = document.getElementById("iva_prod");
      const desc = document.getElementById("desc_prod");
      const cant = document.getElementById("cant_prod");
      iva.value = "";
      desc.value = "";
      cant.value = "";

      for (var i = 0; i < cantidades_productos.length; i++) {
        actualizarValoresdelista(i);
      }
      console.log(iva);
      console.log(desc);
      console.log(cant);
    });
  });

  descuentos.forEach(function (input, index) {
    input.addEventListener("input", function () {
      actualizarValores(index);

      const iva = document.getElementById("iva_prod");
      const desc = document.getElementById("desc_prod");
      const cant = document.getElementById("cant_prod");
      iva.value = "";
      desc.value = "";
      cant.value = "";

      for (var i = 0; i < cantidades_productos.length; i++) {
        actualizarValoresdelista(i);
      }
      console.log(iva);
      console.log(desc);
      console.log(cant);
    });
  });

  function actualizarValoresdelista(i) {
    var value = cantidades_productos[i].value;
    var precio = precios_unitarios[i].value;
    var input2 = total_precio_producto[i];
    var totalProducto = value * precio;

    const iva = document.getElementById("iva_prod");
    const desc = document.getElementById("desc_prod");
    const cant = document.getElementById("cant_prod");

    const currentIndex = cant.value.split(",").length;

    cant.value += (currentIndex > 0 ? "," : "") + value;
    if (descuentos[i].value == 0) {
      desc.value += (currentIndex > 0 ? "," : "") + "0";
      iva.value += (currentIndex > 0 ? "," : "") + totalProducto * 0.1;
    } else {
      desc.value += (currentIndex > 0 ? "," : "") + descuentos[i].value;
      iva.value +=
        (currentIndex > 0 ? "," : "") +
        (totalProducto - (totalProducto * descuentos[i].value) / 100) * 0.1;
    }
  }

  function actualizarValores(index) {
    var value = cantidades_productos[index].value;
    var precio = precios_unitarios[index].value;

    var input2 = total_precio_producto[index];
    var totalProducto = value * precio;
    var iva_pro = totalCompra * 0.1;

    if (descuentos[index].value == 0) {
      input2.value = totalProducto;
    } else {
      totalProducto =
        totalProducto - (totalProducto * descuentos[index].value) / 100;
      input2.value = totalProducto;
    }

    var totalCompra = 0;
    total_compra.value = 0;
    total_precio_producto.forEach(function (input) {
      totalCompra += parseFloat(input.value) || 0;
    });

    total_iva.value = totalCompra * 0.1;
    total_compra.value = totalCompra;
  }

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

  formu_eliminar.forEach(function (input) {
    input.disabled = false;
  });
  $("#anhadir_producto").attr("disabled", false);
  $("#id_detalle").attr("disabled", false);
  $("#finalizar_factura").attr("disabled", false).removeClass("disabled");
  $("#cancelar_factura").attr("disabled", false).removeClass("disabled");

  window.onload = function () {
    var table = document.getElementById("tabla_id");
    var rowCount = table.rows.length;
    console.log("rowCount");
    console.log(rowCount);

    for (var i = 0; i < rowCount; i++) {
      actualizarValoresdelista(i);
    }
  };
});

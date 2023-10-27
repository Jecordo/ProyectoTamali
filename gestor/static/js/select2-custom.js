$(document).ready(function () {
  $("#id_label_multiple").select2({
    tags: true,
    templateResult: function (option) {
      return $('<span style="color: black;">' + option.text + "</span>");
    },
  });

  $("#id_label_multiple").on("change", function () {
    var selectedValue = $(this).val();

    var selectedOption = $(this).find("option:selected");

    var descripcionCompleta = selectedOption.data("descripcion");

    var descripcionArray = descripcionCompleta.split(",");

    var razonSocial = descripcionArray[0].trim();
    var direccion = descripcionArray[1].trim();
    var correo = descripcionArray[2].trim();
    var numTelefono = descripcionArray[3].trim();
    var ruc = descripcionArray[4].trim();

    console.log("Razon Social: " + razonSocial);
    console.log("Direccion: " + direccion);
    console.log("Correo: " + correo);
    console.log("Número de Teléfono: " + numTelefono);
    console.log("RUC: " + ruc);

    $("#razon_social").val(razonSocial);
    $("#direccion_cliente").val(direccion);
    $("#correo_cliente").val(correo);
    $("#num_telefono").val(numTelefono);
    $("#RUC").val(ruc);
  });
});

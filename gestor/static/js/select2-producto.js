$(document).ready(function () {

    $('#cod_producto_id').select2({
        templateResult: function (option) {
            // Aplica estilos CSS personalizados a cada opción
            return $('<span style="color: black;">' + option.text + '</span>');
        }
    });

    $(document).ready(function() {
        // Deshabilita todos los enlaces

        $(window).on("beforeunload", function() {
            // Verifica si la facturación está incompleta
            if (facturaIncompleta) {
              return "Debe finalizar la facturación antes de salir de esta página.";
            }
        });

        $("#finalizar_factura").click(function() {
            // Marca la facturación como completa
            facturaIncompleta = false;
            // Redirige al usuario a una página diferente (puedes personalizar la URL)
        });   

        $("a").attr("disabled", true).addClass("disabled");

        $("button").attr("disabled", true);
    
        // Habilita los botones de "Añadir", "Finalizar" y "Cancelar"
        $("#anhadir_producto").attr("disabled", false);
        $("#id_detalle").attr("disabled", false);
        $("#finalizar_factura").attr("disabled", false).removeClass("disabled");
        $("#cancelar_factura").attr("disabled", false).removeClass("disabled");
      });
      
});
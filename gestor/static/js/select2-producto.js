$(document).ready(function () {

    $('#cod_producto').select2({
        templateResult: function (option) {
            // Aplica estilos CSS personalizados a cada opción
            return $('<span style="color: black;">' + option.text + '</span>');
        }
    });
      
});
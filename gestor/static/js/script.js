document.addEventListener("DOMContentLoaded", function() {
  // Obtener referencias a elementos HTML
  var modal = document.getElementById("myModal");
  var btn = document.getElementById("openModalBtn");
  var span = document.getElementsByClassName("close")[document.getElementsByClassName("close").length - 1];

  var btns_mod = document.querySelectorAll("[id^='openModalBtn_mod_']");
  var spans_close = document.querySelectorAll("[id^='close_']");

  
  // Función para abrir la ventana modal al hacer clic en el botón
  btn.onclick = function() {
    modal.style.display = "block";
  }

  // Función para cerrar la ventana modal al hacer clic en el botón de cierre (X)
  span.onclick = function() {
    modal.style.display = "none";
  }

  // Función para cerrar la ventana modal al hacer clic fuera del contenido de la ventana
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  // Obtener todos los botones de modificación y agregarles un evento onclick
  btns_mod.forEach(function(btn_mod) {
    btn_mod.onclick = function() {
      var productoId = this.getAttribute("data-id"); // Obtener el valor de data-id
      llenarFormularioModal(productoId); // Llenar el formulario modal con los datos del producto
      var modal_mod = document.getElementById("myModal_mod_" + productoId);
      modal_mod.style.display = "block"; // Mostrar el modal correspondiente
    }
  });


  spans_close.forEach(function(span_close) {
    span_close.onclick = function() {
      var productoId = this.getAttribute("data-id"); // Obtener el valor de data-id
      var modal_mod = document.getElementById("myModal_mod_" + productoId);
      modal_mod.style.display = "none"; // Ocultar el modal correspondiente
    }
  });


  function llenarFormularioModal(productoId) {
    // Obtener la descripción del producto del atributo data-descripcion del botón
    var descripcion = document.getElementById("openModalBtn_mod_" + productoId).getAttribute("data-descripcion");
    var descripcionarray = descripcion.split(",");
    
    console.log(descripcionarray)
    document.getElementById("cod_producto_mod_" + productoId).value = descripcionarray[0];
    document.getElementById("desc_producto_mod_" + productoId).value = descripcionarray[1];
    document.getElementById("precio_venta_mod_" + productoId).value = descripcionarray[2];
    document.getElementById("precio_compra_mod_" + productoId).value = descripcionarray[3];

    var selectProv = document.getElementById("prov_producto_mod_" + productoId);
    var valorProv = descripcionarray[4].trim();

    var selectCat = document.getElementById("categoria_producto_mod_" + productoId);
    var valorCat = descripcionarray[5].trim();

    var selectMarc = document.getElementById("marca_producto_mod_" + productoId);
    var valorMarc = descripcionarray[6].trim();
    var marc = valorMarc+'_'+productoId

    for (var i = 0; i < selectProv.options.length; i++) {
      if (selectProv.options[i].value === valorProv) {
        selectProv.options[i].selected = true;
        break;
      }
    }

    for (var i = 0; i < selectCat.options.length; i++) {
      if (selectCat.options[i].value === valorCat) {
        selectCat.options[i].selected = true;
        break;
      }
    }

    console.log(selectMarc)
    console.log(marc)
    for (var i = 0; i < selectMarc.options.length; i++) {
      if (selectMarc.options[i].value === marc) {
        selectMarc.options[i].selected = true;
        break;
      }
    }

  }
});

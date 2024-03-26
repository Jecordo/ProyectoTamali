// Obtener referencias a elementos HTML
var modal = document.getElementById("myModal");
var modal2 = document.getElementById("myModal_mod");
var btn = document.getElementById("openModalBtn");
var btn2 = document.getElementById("openModalBtn_mod");
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementById("close");

// Función para abrir la ventana modal al hacer clic en el botón
btn.onclick = function() {
  modal.style.display = "block";
}

btn2.onclick = function() {
  modal2.style.display = "block";
}

// Función para cerrar la ventana modal al hacer clic en el botón de cierre (X)
span.onclick = function() {
  modal.style.display = "none";
}

span2.onclick = function() {
  modal2.style.display = "none";
}

// Función para cerrar la ventana modal al hacer clic fuera del contenido de la ventana
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }

  if (event.target == modal2) {
    modal2.style.display = "none";
  }
}

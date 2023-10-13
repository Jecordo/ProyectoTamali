function agregarFila() {
    const container = document.getElementById('container');
    const rows = container.querySelectorAll('.row');
    const newRow = rows[0].cloneNode(true);
  
    // Obtener el número de filas actual
    const numRows = rows.length + 1;
  
    // Actualizar los nombres de los campos clonados
    newRow.querySelectorAll('[name]').forEach(field => {
      const fieldName = field.getAttribute('name');
      field.setAttribute('name', `${fieldName}_${numRows}`);
    });
  
    container.appendChild(newRow);
  }
  
  
  document.getElementById('eliminarFila').addEventListener('click', function() {
    const container = document.getElementById('container');
    const rows = container.querySelectorAll('.row');
    
    // Asegurarse de que al menos haya una fila en el contenedor
    if (rows.length > 1) {
      container.removeChild(rows[rows.length - 1]);
    }
    
  });
  
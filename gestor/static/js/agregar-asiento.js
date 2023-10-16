
        
        
document.addEventListener('DOMContentLoaded', function () {
    const dataForm = document.getElementById("dataForm");
    const tablaDatos = document.getElementById("tablaDatos");
    const fechaEmision = document.getElementById("fecha_emision");
    const fechaEmisionHidden = document.getElementById("fecha_emision_hidden");

    let idCounter = 1; 
    
    fechaEmision.addEventListener("change", function () {
        fechaEmisionHidden.value = fechaEmision.value;
    });

    function agregarFila(id_concepto, num_cuenta, tipo_movimiento, id_monto, cuenta_descripcion) {
        const newRow = tablaDatos.insertRow(tablaDatos.rows.length);
        const cellConcepto = newRow.insertCell(0);
        const cellCuenta = newRow.insertCell(1);
        const cellCuentaDescrip = newRow.insertCell(2);
        const cellDebe = newRow.insertCell(3);
        const cellHaber = newRow.insertCell(4);
        const cellOption = newRow.insertCell(5);



        cellConcepto.name = "concepto-" + idCounter;
        cellConcepto.innerHTML = id_concepto;
        cellCuenta.name = "cuenta-" + idCounter;
        cellCuenta.innerHTML = num_cuenta;
        cellCuentaDescrip.innerHTML = cuenta_descripcion;
        if (tipo_movimiento === "1") {
            cellDebe.id = "debe-" + idCounter;
            cellDebe.innerHTML = dataForm.id_monto.value;
            cellHaber.id = "haber-" + idCounter;
            cellHaber.innerHTML = 0;
        }else if ((tipo_movimiento === "2")) {
            cellDebe.id = "debe-" + idCounter;
            cellDebe.innerHTML = 0;
            cellHaber.id = "haber-" + idCounter;
            cellHaber.innerHTML = dataForm.id_monto.value;
        }

        const eliminarBtn = document.createElement("button");
        eliminarBtn.textContent = "Eliminar";
        eliminarBtn.addEventListener("click", function () {
            tablaDatos.deleteRow(newRow.rowIndex);
            totales();
        });
        cellOption.appendChild(eliminarBtn);

        newRow.id = "row-" + idCounter; 
        idCounter++; 
    }

    function totales() {
        var diferencia = 0;
        var total_debe = 0;
        var total_haber = 0;
        
        for (var i = 0; i < tablaDatos.rows.length; i++) { 
            var debe = parseFloat(tablaDatos.rows[i].cells[3].textContent); 
            var haber = parseFloat(tablaDatos.rows[i].cells[4].textContent); 
    
            if (!isNaN(debe)) {
                total_debe += debe;
            }
            if (!isNaN(haber)) {
                total_haber += haber;
            }
        }
        diferencia = total_debe - total_haber;
        document.getElementById("tdiferencia").value = diferencia;
    }

    dataForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const id_concepto = dataForm.id_concepto.value;
        const numCuentaDescripcion = dataForm.num_cuenta.value.split(',');
        const num_cuenta = numCuentaDescripcion[0];
        const cuenta_descripcion = numCuentaDescripcion[1];
        const tipo_movimiento = dataForm.tipo_movimiento.value;
        const id_monto = dataForm.id_monto.value;
        const fecha_emision = dataForm.fecha_emision.value;

        if (!id_concepto || !num_cuenta || !tipo_movimiento || !id_monto || !cuenta_descripcion) {
            alert("Por favor, ingresa todos los campos.");
            return;
        }

        agregarFila(id_concepto, num_cuenta, tipo_movimiento, id_monto, cuenta_descripcion);

        dataForm.reset();

        totales();

        dataForm.id_concepto.value = id_concepto;
        dataForm.fecha_emision.value = fecha_emision;
    });

    function enviarTablaAlBackend() {
        const filas = tablaDatos.rows;
        const fecha_emision_hidden = document.getElementById("fecha_emision_hidden").value;
    
        const datos = [];
    
        for (let i = 1; i < filas.length; i++) {
            const fila = filas[i];
            const concepto = fila.cells[0].textContent;
            const numCuenta = fila.cells[1].textContent;
            const descripcion = fila.cells[2].textContent;
            const debe = parseFloat(fila.cells[3].textContent);
            const haber = parseFloat(fila.cells[4].textContent);
    
            datos.push({ concepto, numCuenta, descripcion, debe, haber, fecha_emision_hidden});
        }


        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch('/gestor/cargar_libro_diario/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ datos })
        })
        .then(response => {
        })
        .catch(error => {
            console.error('Error al enviar datos al backend: ', error);
        });
    }

    document.getElementById("agregarAsientoButton").addEventListener("click", function(event) {
        event.preventDefault();

        totales();

        if (parseFloat(document.getElementById("tdiferencia").value) !== 0) {
            alert("La diferencia debe ser igual a 0 para agregar el asiento.");
        } else {
            // Envía los datos de la tabla al backend
            enviarTablaAlBackend();
        }
    });

});
        

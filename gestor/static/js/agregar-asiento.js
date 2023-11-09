document.addEventListener("DOMContentLoaded", function () {
  const dataForm = document.getElementById("dataForm");
  const tablaDatos = document.getElementById("tablaDatos");
  const fechaEmision = document.getElementById("fecha_emision");
  const fechaEmisionHidden = document.getElementById("fecha_emision_hidden");
  var fromu = document.getElementById("fromu");

  let idCounter = 1;

  fechaEmision.addEventListener("change", function () {
    fechaEmisionHidden.value = fechaEmision.value;
  });

  function agregarFila(
    id_concepto,
    num_cuenta,
    tipo_movimiento,
    id_monto,
    cuenta_descripcion
  ) {
    const newRow = tablaDatos.insertRow(tablaDatos.rows.length);
    const cellConcepto = newRow.insertCell(0);
    const cellCuenta = newRow.insertCell(1);
    const cellCuentaDescrip = newRow.insertCell(2);
    const cellDebe = newRow.insertCell(3);
    const cellHaber = newRow.insertCell(4);
    const cellOption = newRow.insertCell(5);

    const conceptosHidden = document.getElementById("concepto-hidden");
    const cuentasHidden = document.getElementById("cuenta-hidden");
    const debesHidden = document.getElementById("debe-hidden");
    const haberesHidden = document.getElementById("haber-hidden");

    const currentIndex = conceptosHidden.value.split(",").length;

    conceptosHidden.value += (currentIndex > 0 ? "," : "") + id_concepto;
    cuentasHidden.value += (currentIndex > 0 ? "," : "") + num_cuenta;

    cellConcepto.innerHTML = id_concepto;
    cellCuenta.innerHTML = num_cuenta;
    cellCuentaDescrip.innerHTML = cuenta_descripcion;
    if (tipo_movimiento === "1") {
      debesHidden.value += (currentIndex > 0 ? "," : "") + id_monto;
      haberesHidden.value += (currentIndex > 0 ? "," : "") + "0";

      cellDebe.innerHTML = dataForm.id_monto.value;
      cellHaber.innerHTML = 0;
    } else if (tipo_movimiento === "2") {
      debesHidden.value += (currentIndex > 0 ? "," : "") + "0";
      haberesHidden.value += (currentIndex > 0 ? "," : "") + id_monto;

      cellDebe.innerHTML = 0;
      cellHaber.innerHTML = dataForm.id_monto.value;
    }

    const eliminarBtn = document.createElement("button");
    eliminarBtn.textContent = "Eliminar";
    eliminarBtn.addEventListener("click", function () {
      tablaDatos.deleteRow(newRow.rowIndex);

      const conceptosHidden = document.getElementById("concepto-hidden");
      const cuentasHidden = document.getElementById("cuenta-hidden");
      const debesHidden = document.getElementById("debe-hidden");
      const haberesHidden = document.getElementById("haber-hidden");

      const conceptosArray = conceptosHidden.value.split(",");
      const cuentasArray = cuentasHidden.value.split(",");
      const debesArray = debesHidden.value.split(",");
      const haberesArray = haberesHidden.value.split(",");

      const index = newRow.rowIndex - 1;

      conceptosArray.splice(index, 1);
      cuentasArray.splice(index, 1);
      debesArray.splice(index, 1);
      haberesArray.splice(index, 1);

      conceptosHidden.value = conceptosArray.join(",");
      cuentasHidden.value = cuentasArray.join(",");
      debesHidden.value = debesArray.join(",");
      haberesHidden.value = haberesArray.join(",");

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

  dataForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const id_concepto = dataForm.id_concepto.value;
    const numCuentaDescripcion = dataForm.num_cuenta.value.split(",");
    const num_cuenta = numCuentaDescripcion[0];
    const cuenta_descripcion = numCuentaDescripcion[1];
    const tipo_movimiento = dataForm.tipo_movimiento.value;
    const id_monto = dataForm.id_monto.value;
    const fecha_emision = dataForm.fecha_emision.value;

    if (
      !id_concepto ||
      !num_cuenta ||
      !tipo_movimiento ||
      !id_monto ||
      !cuenta_descripcion
    ) {
      alert("Por favor, ingresa todos los campos.");
      return;
    }

    agregarFila(
      id_concepto,
      num_cuenta,
      tipo_movimiento,
      id_monto,
      cuenta_descripcion
    );

    dataForm.reset();

    totales();

    dataForm.id_concepto.value = id_concepto;
    dataForm.fecha_emision.value = fecha_emision;
  });

  fromu.addEventListener("submit", function (event) {
    event.preventDefault();
    const conceptosHidden = document.getElementById("concepto-hidden");

    totales();

    if (parseFloat(document.getElementById("tdiferencia").value) !== 0) {
      alert("La diferencia debe ser igual a 0 para agregar el asiento.");
    } else {
      if (conceptosHidden.value.length < 1) {
        alert("El asiento esta vacio.");
      } else {
        fromu.submit();
      }
    }
  });

    function onPageLoad(cabe_lib) {
        const detalleHidden = document.getElementById("detalle-hidden"); 
        const detalle = JSON.parse(detalleHidden.value);
        const dataForm = document.getElementById("dataForm");
        const aux = document.getElementById("cabe_lib").value;
        const partes = aux.split(' - ');
        const fecha = new Date(partes[0]); // Convierte la primera parte en un objeto de fecha
        const fecha_cab = fecha.toISOString().slice(0, 10);
        const concepto_cab = partes[1];
        const tablaDatos = document.getElementById("tablaDatos"); 
        let idCounter = 1; 
    
        detalle.forEach(function (det) {
            const newRow = tablaDatos.insertRow(tablaDatos.rows.length);
            const cellConcepto = newRow.insertCell(0);
            const cellCuenta = newRow.insertCell(1);
            const cellCuentaDescrip = newRow.insertCell(2);
            const cellDebe = newRow.insertCell(3);
            const cellHaber = newRow.insertCell(4);
            const cellOption = newRow.insertCell(5);

      cellConcepto.innerHTML = det.concepto;
      cellCuenta.innerHTML = det.num_cuenta.num_cuenta;
      cellCuentaDescrip.innerHTML = det.num_cuenta.descripcion;
      cellDebe.innerHTML = det.debe;
      cellHaber.innerHTML = det.haber;

      const eliminarBtn = document.createElement("button");
      eliminarBtn.textContent = "Eliminar";
      eliminarBtn.addEventListener("click", function () {
        tablaDatos.deleteRow(newRow.rowIndex);

        const conceptosHidden = document.getElementById("concepto-hidden");
        const cuentasHidden = document.getElementById("cuenta-hidden");
        const debesHidden = document.getElementById("debe-hidden");
        const haberesHidden = document.getElementById("haber-hidden");

        const conceptosArray = conceptosHidden.value.split(",");
        const cuentasArray = cuentasHidden.value.split(",");
        const debesArray = debesHidden.value.split(",");
        const haberesArray = haberesHidden.value.split(",");

        const index = newRow.rowIndex - 1;

        conceptosArray.splice(index, 1);
        cuentasArray.splice(index, 1);
        debesArray.splice(index, 1);
        haberesArray.splice(index, 1);

        conceptosHidden.value = conceptosArray.join(",");
        cuentasHidden.value = cuentasArray.join(",");
        debesHidden.value = debesArray.join(",");
        haberesHidden.value = haberesArray.join(",");

        totales();
      });
      cellOption.appendChild(eliminarBtn);

      newRow.id = "row-" + idCounter;
      idCounter++;
    });

    dataForm.id_concepto.value = concepto_cab;
    dataForm.fecha_emision.value = fecha_cab;

    fechaEmisionHidden.value = fechaEmision.value;

    totales();
  }

  onPageLoad(cabe_lib);
});

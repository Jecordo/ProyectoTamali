let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { orderable: false, targets: [0] },
        { searchable: false, targets: [4] }
    ],
    pageLength: 4,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    dataTable = $("#tabla_id").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};



window.addEventListener("load", async () => {
    await initDataTable();
});
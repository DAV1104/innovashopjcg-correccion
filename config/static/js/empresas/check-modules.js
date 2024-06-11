document.addEventListener("DOMContentLoaded", function() {
    const empresaId = window.empresaId;

    if (!empresaId) {
        console.error("No empresaId found");
        return;
    }

    fetch(`/empresa/${empresaId}/modules`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error fetching modules:', data.error);
            return;
        }

        const modules = data.modules;

        // Show or hide elements based on module states
        if (!modules.clientes) {
            document.querySelector('.icon-clientes').style.display = 'none';
        }
        if (!modules.vendedores) {
            document.querySelector('.icon-vendedores').style.display = 'none';
        }
        if (!modules.cotizaciones) {
            document.querySelector('.icon-cotizacion').style.display = 'none';
        }
        if (!modules.stock) {
            document.querySelector('.icon-stock').style.display = 'none';
        }
        if (!modules.proveedores) {
            document.querySelector('.icon-proveedores').style.display = 'none';
        }

        // Specific case for hiding the "Añadir Stock" button in stock-empresas.html
        if (!modules.compras) {
            const addStockButton = document.getElementById('add-stock-button');
            if (addStockButton) {
                addStockButton.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error fetching modules:', error);
    });
});

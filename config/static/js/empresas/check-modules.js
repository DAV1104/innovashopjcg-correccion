document.addEventListener("DOMContentLoaded", function() {
    const empresaId = // Set this to the current empresa_id (you might need to get it from the session or a global variable);
    
    fetch(`/ruta_empresa/${empresaId}/modules`, {
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
        if (!modules.compras) {
            // Assuming you want to hide the entire compras container
            document.querySelector('.container').style.display = 'none';
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
        if (!modules.stock) {
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

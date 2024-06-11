document.addEventListener('DOMContentLoaded', function() {
    axios.get('/admin/admin-info')
        .then(function(response) {
            document.getElementById('admin-name').textContent = response.data.nombre;
        })
        .catch(function(error) {
            console.error('Error fetching admin info:', error);
            document.getElementById('admin-name').textContent = 'Error';
        });

    const searchInput = document.querySelector('.search-bar input[name="query"]');
    const companiesList = document.querySelector('#companies-list');
    const accordion = document.getElementById('accordionExample');
    const moduleCheckboxes = {
        'clientes': document.getElementById('clientes-modulo'),
        'vendedores': document.getElementById('vendedores-modulo'),
        'compras': document.getElementById('compras-modulo'),
        'cotizaciones': document.getElementById('cotizaciones-modulo'),
        'stock': document.getElementById('stock-modulo'),
        'informes': document.getElementById('informes-modulo')
    };
    let selectedEmpresaId = null;
    let debounceTimeout;

    const performSearch = () => {
        const query = searchInput.value;
        axios.get(`/admin/search-empresas?query=${encodeURIComponent(query)}`)
            .then(function(response) {
                const enterprises = response.data;
                const tableBody = companiesList;
                tableBody.innerHTML = '';

                enterprises.forEach(empresa => {
                    const tr = document.createElement('tr');
                    tr.dataset.empresaId = empresa.id;
                    tr.dataset.nit = empresa.nit;
                    tr.dataset.nombre = empresa.nombre;

                    const idTd = document.createElement('td');
                    idTd.textContent = empresa.nit;
                    tr.appendChild(idTd);

                    const nombreTd = document.createElement('td');
                    nombreTd.textContent = empresa.nombre;
                    tr.appendChild(nombreTd);

                    const accionesTd = document.createElement('td');
                    const viewButton = document.createElement('button');
                    viewButton.classList.add('btn', 'btn-primary', 'btn-view-modules');
                    viewButton.textContent = 'Ver Modulos';
                    viewButton.addEventListener('click', (event) => {
                        event.stopPropagation();
                        document.querySelectorAll('tbody tr').forEach(row => row.classList.remove('selected'));
                        tr.classList.add('selected');
                        selectEmpresa(empresa.id);
                    });
                    accionesTd.appendChild(viewButton);
                    tr.appendChild(accionesTd);

                    tableBody.appendChild(tr);
                });
            })
            .catch(function(error) {
                console.error('Error fetching enterprises:', error);
            });
    };

    const selectEmpresa = (empresaId) => {
        selectedEmpresaId = empresaId;

        axios.get(`/empresa/${empresaId}/modules`)
            .then(function(response) {
                const modules = response.data.modules || {};
                Object.keys(moduleCheckboxes).forEach(moduleName => {
                    moduleCheckboxes[moduleName].checked = modules[moduleName] || false;
                });
                accordion.classList.remove('hidden');
            })
            .catch(function(error) {
                console.error('Error fetching modules:', error);
            });
    };

    const updateModuleStatus = (moduleName, status) => {
        if (!selectedEmpresaId) {
            console.error('No empresa selected');
            return;
        }

        axios.post('/empresa/update-module-status', { empresaId: selectedEmpresaId, moduloNombre: moduleName, estado: status })
            .then(function(response) {
                console.log('Module status updated');
            })
            .catch(function(error) {
                console.error('Error updating module status:', error);
            });
    };

    Object.keys(moduleCheckboxes).forEach(moduleName => {
        moduleCheckboxes[moduleName].addEventListener('change', (event) => {
            updateModuleStatus(moduleName, event.target.checked);
        });
    });

    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(performSearch, 300);
    });

    performSearch(); // Initial load
});

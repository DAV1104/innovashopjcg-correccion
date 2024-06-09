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
    let selectedEmpresaId = null;
    let debounceTimeout;

    const performSearch = () => {
        const query = searchInput.value.trim();

        axios.get(`/admin/search-empresas?query=${encodeURIComponent(query)}`)
            .then(function(response) {
                const enterprises = response.data;
                const tableBody = document.querySelector('#companies-list');
                tableBody.innerHTML = '';

                enterprises.forEach(empresa => {
                    const tr = document.createElement('tr');
                    tr.dataset.id = empresa.id;
                    tr.dataset.nit = empresa.nit;
                    tr.dataset.nombre = empresa.nombre;

                    const nitTd = document.createElement('td');
                    nitTd.textContent = empresa.nit;
                    tr.appendChild(nitTd);

                    const nombreTd = document.createElement('td');
                    nombreTd.textContent = empresa.nombre;
                    tr.appendChild(nombreTd);

                    const ivaTd = document.createElement('td');
                    ivaTd.textContent = empresa.tax;
                    tr.appendChild(ivaTd);

                    const gananciaTd = document.createElement('td');
                    gananciaTd.textContent = empresa.profit_percentage;
                    tr.appendChild(gananciaTd);

                    const accionesTd = document.createElement('td');
                    const verPorcentajesBtn = document.createElement('button');
                    verPorcentajesBtn.classList.add('btn-ver-modulos', 'btn');
                    verPorcentajesBtn.textContent = 'Ver Porcentajes';
                    verPorcentajesBtn.dataset.id = empresa.id;
                    verPorcentajesBtn.addEventListener('click', () => selectEmpresa(empresa.id));
                    accionesTd.appendChild(verPorcentajesBtn);
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

        axios.get(`/empresa/${empresaId}/percentages`)
            .then(function(response) {
                const { iva, ganancia } = response.data;
                document.getElementById('iva').value = iva || '';
                document.getElementById('ganancia').value = ganancia || '';
                document.getElementById('accordionCito').classList.remove('hidden');
            })
            .catch(function(error) {
                console.error('Error fetching percentages:', error);
            });
    };

    const updatePercentages = () => {
        const iva = document.getElementById('iva').value;
        const ganancia = document.getElementById('ganancia').value;

        if (!selectedEmpresaId) {
            alert('Seleccione una empresa primero');
            return;
        }

        axios.post(`/empresa/update-percentages`, {
            empresaId: selectedEmpresaId,
            iva: parseFloat(iva),
            ganancia: parseFloat(ganancia)
        })
        .then(function(response) {
            alert('Percentages updated successfully');
            performSearch();
        })
        .catch(function(error) {
            console.error('Error updating percentages:', error);
        });
    };

    document.querySelector('.accordion .percentages button').addEventListener('click', updatePercentages);

    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(performSearch, 300);
    });

    // Initial load
    performSearch();
});

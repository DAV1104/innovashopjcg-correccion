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
    const agregarButton = document.querySelector('.btn-agregar');
    let selectedNit = null;
    let selectedNombre = null;

    const performSearch = () => {
        const query = searchInput.value;
        axios.get(`/admin/search-empresas?query=${encodeURIComponent(query)}`)
            .then(function(response) {
                const enterprises = response.data;
                const tableBody = document.querySelector('tbody');
                tableBody.innerHTML = '';

                enterprises.forEach(empresa => {
                    const tr = document.createElement('tr');
                    tr.dataset.nit = empresa.nit;
                    tr.dataset.nombre = empresa.nombre;

                    const idTd = document.createElement('td');
                    idTd.textContent = empresa.nit;
                    tr.appendChild(idTd);

                    const nombreTd = document.createElement('td');
                    nombreTd.textContent = empresa.nombre;
                    tr.appendChild(nombreTd);

                    const estadoTd = document.createElement('td');
                    const estadoSpan = document.createElement('span');
                    estadoSpan.style.borderRadius = '50%';
                    estadoSpan.style.width = '20px';
                    estadoSpan.style.height = '20px';
                    estadoSpan.style.display = 'inline-block';
                    estadoSpan.style.backgroundColor = empresa.estado === 'activo' ? '#00ff00' : '#ff0000';
                    estadoTd.appendChild(estadoSpan);
                    tr.appendChild(estadoTd);

                    const ultimaSesionTd = document.createElement('td');
                    ultimaSesionTd.textContent = empresa.ultima_sesion;
                    tr.appendChild(ultimaSesionTd);

                    const sessionLimitTd = document.createElement('td');
                    sessionLimitTd.textContent = new Date(empresa.session_limit).toLocaleDateString();
                    tr.appendChild(sessionLimitTd);

                    tr.addEventListener('click', () => {
                        selectedNit = empresa.nit;
                        selectedNombre = empresa.nombre;
                        document.querySelectorAll('tr').forEach(row => row.classList.remove('selected'));
                        tr.classList.add('selected');
                    });

                    tableBody.appendChild(tr);
                });
            })
            .catch(function(error) {
                console.error('Error fetching enterprises:', error);
            });
    };

    const updateEmpresaEstado = (estado) => {
        if (!selectedNit || !selectedNombre) {
            alert('Seleccione una empresa para cambiar el estado.');
            return;
        }

        axios.post('/admin/update-empresa-estado', {
            nit: selectedNit,
            nombre: selectedNombre,
            estado: estado
        })
        .then(function(response) {
            performSearch();
        })
        .catch(function(error) {
            console.error('Error updating empresa estado:', error);
        });
    };

    document.querySelector('.btn-habilitar').addEventListener('click', () => {
        updateEmpresaEstado('activo');
    });

    document.querySelector('.btn-deshabilitar').addEventListener('click', () => {
        updateEmpresaEstado('inactivo');
    });

    agregarButton.addEventListener('click', (event) => {
        event.preventDefault();
        window.location.href = '/admin/admin-add-empresas';
    });

    searchInput.addEventListener('input', performSearch);

    // Initial load
    performSearch();
});

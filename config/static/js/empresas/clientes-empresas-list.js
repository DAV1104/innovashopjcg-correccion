document.addEventListener('DOMContentLoaded', function() {
    const checkStatusAndUpdateInfo = () => {
        axios.get('/empresa/empresa-info')
            .then(function(response) {
                const empresaData = response.data;
                document.getElementById('empresa-name').textContent = empresaData.nombre;
                document.getElementById('empresa-rol').textContent = empresaData.rol;

                if (empresaData.estado !== 'activo') {
                    Swal.fire({
                        icon: 'error',
                        title: 'Empresa Inactiva',
                        text: 'La empresa se encuentra inactiva. Por favor, solicite más tiempo de acceso.',
                        allowOutsideClick: false,
                        allowEscapeKey: false
                    }).then(() => {
                        window.location.href = '/user/login';
                    });
                }
            })
            .catch(function(error) {
                console.error('Error fetching empresa info:', error);
                document.getElementById('empresa-name').textContent = 'Error';
            });
    };

    // Initial check
    checkStatusAndUpdateInfo();

    const searchInput = document.querySelector('.search-bar input[name="query"]');

    const performSearch = () => {
        const query = searchInput.value;
        axios.get(`/empresa/api/clientes?query=${encodeURIComponent(query)}`)
            .then(function(response) {
                const usuarios = response.data;
                const tableBody = document.querySelector('tbody');
                tableBody.innerHTML = '';

                usuarios.forEach(usuario => {
                    const tr = document.createElement('tr');
                    tr.dataset.id = usuario.id;

                    const cedulaTd = document.createElement('td');
                    cedulaTd.textContent = usuario.cedula;
                    tr.appendChild(cedulaTd);

                    const nombreTd = document.createElement('td');
                    nombreTd.textContent = `${usuario.nombre} ${usuario.apellidos}`;
                    tr.appendChild(nombreTd);

                    const telefonoTd = document.createElement('td');
                    telefonoTd.textContent = usuario.telefono;
                    tr.appendChild(telefonoTd);

                    const emailTd = document.createElement('td');
                    emailTd.textContent = usuario.email;
                    tr.appendChild(emailTd);

                    tableBody.appendChild(tr);
                });
            })
            .catch(function(error) {
                console.error('Error fetching usuarios:', error);
            });
    };

    searchInput.addEventListener('input', performSearch);

    // Initial load
    performSearch();

    // Check status periodically
    setInterval(checkStatusAndUpdateInfo, 60000); // Check every minute
});

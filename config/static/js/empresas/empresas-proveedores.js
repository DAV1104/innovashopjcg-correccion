document.addEventListener('DOMContentLoaded', function() {
    const empresaNameElem = document.getElementById('empresa-name');
    const empresaRolElem = document.getElementById('empresa-rol');

    const checkStatusAndUpdateInfo = () => {
        axios.get('/empresa/empresa-info')
            .then(function(response) {
                const empresaData = response.data;
                empresaNameElem.textContent = empresaData.nombre;
                empresaRolElem.textContent = empresaData.rol;

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
                empresaNameElem.textContent = 'Error';
            });
    };

    const loadProveedores = () => {
        axios.get('/proveedor/proveedores-list')
            .then(function(response) {
                const proveedoresList = document.getElementById('companies-list');
                proveedoresList.innerHTML = '';
                response.data.forEach(proveedor => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${proveedor.id}</td>
                        <td>${proveedor.nombre}</td>
                        <td>${proveedor.telefono}</td>
                        <td>${proveedor.contacto}</td>
                    `;
                    proveedoresList.appendChild(row);
                });
            })
            .catch(function(error) {
                console.error('Error fetching proveedores:', error);
            });
    };

    // Initial check
    checkStatusAndUpdateInfo();
    loadProveedores();

    // Set an interval to check the status every 30 seconds (30000 milliseconds)
    setInterval(checkStatusAndUpdateInfo, 30000); // 30 seconds
});

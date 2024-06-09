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

    const performSearch = () => {
        const query = searchInput.value;
        axios.get(`/api/clientes?query=${encodeURIComponent(query)}`)
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
});

document.addEventListener("DOMContentLoaded", function() {
    fetch('/vendedor/vendedores', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('companies-list');
        tbody.innerHTML = ''; // Clear existing rows

        data.forEach(vendedor => {
            const row = document.createElement('tr');

            const cedulaCell = document.createElement('td');
            cedulaCell.textContent = vendedor.cedula;
            row.appendChild(cedulaCell);

            const nombreCell = document.createElement('td');
            nombreCell.textContent = vendedor.nombre;
            row.appendChild(nombreCell);

            const telefonoCell = document.createElement('td');
            telefonoCell.textContent = vendedor.telefono;
            row.appendChild(telefonoCell);

            const emailCell = document.createElement('td');
            emailCell.textContent = vendedor.email;
            row.appendChild(emailCell);

            tbody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching vendors:', error);
    });

    document.getElementById('addVendedorForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const cedula = document.getElementById('cedula').value;
        const nombre = document.getElementById('nombre').value;
        const apellidos = document.getElementById('apellidos').value;
        const telefono = document.getElementById('telefono').value;
        const email = document.getElementById('email').value;
        const usuario = document.getElementById('usuario').value;
        const contraseña = document.getElementById('contraseña').value;
        const direccion = document.getElementById('direccion').value;

        const data = {
            cedula: cedula,
            nombre: nombre,
            apellidos: apellidos,
            telefono: telefono,
            email: email,
            usuario: usuario,
            contraseña: contraseña,
            direccion: direccion,
            rol: 'vendedor'
        };

        fetch('/vendedor/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Vendedor agregado con éxito');
                location.reload();
            } else {
                alert('Error al agregar vendedor: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al agregar vendedor');
        });
    });
});

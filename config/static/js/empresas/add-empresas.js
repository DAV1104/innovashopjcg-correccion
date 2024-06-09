document.addEventListener('DOMContentLoaded', function() {
    axios.get('/admin/admin-info')
        .then(function(response) {
            document.getElementById('admin-name').textContent = response.data.nombre;
        })
        .catch(function(error) {
            console.error('Error fetching admin info:', error);
            document.getElementById('admin-name').textContent = 'Error';
        });

    document.querySelector('.new-empresa-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const inputs = document.querySelectorAll('.inputs input');
        let allFilled = true;
        let validDate = true;

        inputs.forEach(input => {
            if (!input.value) {
                allFilled = false;
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }

            if (input.id === 'session_limit') {
                const dateValue = new Date(input.value);
                if (isNaN(dateValue.getTime())) {
                    validDate = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            }
        });

        if (!allFilled) {
            alert('Todos los campos son obligatorios!');
            return;
        }

        if (!validDate) {
            alert('Fecha de límite de sesiones no válida!');
            return;
        }

        const empresaData = {
            nombre: document.getElementById('nombre').value,
            direccion: document.getElementById('direccion').value,
            telefono: document.getElementById('telefono').value,
            email: document.getElementById('email').value,
            usuario: document.getElementById('usuario').value,
            contraseña: document.getElementById('contraseña').value,
            nit: document.getElementById('nit').value,
            session_limit: document.getElementById('session_limit').value,
            general_discount: document.getElementById('general_discount').value,
            tax: document.getElementById('tax').value,
            profit_percentage: document.getElementById('profit_percentage').value
        };

        axios.post('/empresa/register', empresaData)
            .then(function(response) {
                alert('Empresa registrada con éxito!');
                window.location.href = '/admin/admin-empresas';
            })
            .catch(function(error) {
                if (error.response && error.response.status === 409) {
                    alert('La empresa ya existe con el mismo nombre, usuario, email o NIT.');
                } else {
                    console.error('Error registering empresa:', error);
                    alert('Error registrando la empresa.');
                }
            });
    });
});

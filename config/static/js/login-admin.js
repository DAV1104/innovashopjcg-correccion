document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            console.log('Form submission triggered'); // Debugging log

            let userInput = document.getElementById("usuario");
            let passInput = document.getElementById("password");

            console.log('Input elements:', userInput, passInput); // Debugging log

            let user = userInput.value;
            let password = passInput.value;

            console.log('Input values:', { user, password }); // Debugging log

            if (!user || !password) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Todos los campos son obligatorios!',
                });
                return;
            }

            let endpoint = "/auth/ingreso-admin";  // Ensure this matches your route in Flask

            console.log('Sending POST request to:', endpoint); // Debugging log

            axios.post(endpoint, {
                'usuario': user,
                'clave': password
            })
            .then(function (response) {
                console.log('Response received:', response); // Log the response
                if (response.data.success) {
                    console.log('Successful login, setting token and redirecting...');
                    document.cookie = `token=${response.data.token}; path=/;`;
                    Swal.fire({
                        icon: 'success',
                        title: '¡Inicio de sesión exitoso!',
                        text: 'Redirigiendo...',
                        timer: 2000,
                        timerProgressBar: true,
                        showConfirmButton: false
                    }).then(() => {
                        window.location.href = "/admin/home";
                    });
                } else {
                    console.log('Login failed, showing error message...');
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.data.error || 'Error desconocido'
                    });
                    console.error('Error:', response.data.error || 'Error desconocido');
                }
            })
            .catch(function (error) {
                console.error('Error validating user:', error); // Log the error
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.response?.data?.error || 'Ha ocurrido un error al validar el usuario.'
                });
            });
        });
    } else {
        console.error('Login form not found!');
    }
});

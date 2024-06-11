document.addEventListener("DOMContentLoaded", function() {
    fetch('/ruta_vendedor/vendedor/info', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error fetching vendor info:', data.error);
            return;
        }

        document.getElementById('vendedor-name').textContent = data.nombre;
        document.getElementById('vendedor-rol').textContent = data.rol;
    })
    .catch(error => {
        console.error('Error fetching vendor info:', error);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const checkStatusAndUpdateInfo = () => {
      axios
        .get("/empresa/empresa-info")
        .then(function (response) {
          const empresaData = response.data;
          document.getElementById("empresa-name").textContent = empresaData.nombre;
          document.getElementById("empresa-rol").textContent = empresaData.rol;
  
          if (empresaData.estado !== "activo") {
            Swal.fire({
              icon: "error",
              title: "Empresa Inactiva",
              text: "La empresa se encuentra inactiva. Por favor, solicite más tiempo de acceso.",
              allowOutsideClick: false,
              allowEscapeKey: false,
            }).then(() => {
              window.location.href = "/user/login";
            });
          }
        })
        .catch(function (error) {
          console.error("Error fetching empresa info:", error);
          document.getElementById("empresa-name").textContent = "Error";
        });
    };
  
    // Initial check
    checkStatusAndUpdateInfo();

    const searchInput = document.getElementById("search-bar");
    const cartButton = document.getElementById("cart-button");
    const clearCartButton = document.getElementById("clear-cart-button");
    const checkoutButton = document.getElementById("checkout-button");
    const productContainer = document.getElementById("product-list");
    const cartItemsContainer = document.querySelector(".cart-items-container");
    const stockForm = document.getElementById("add-stock-form");

    let cart = [];
  
    const fetchProducts = () => {
      axios
        .get("/producto/productos") // Using the prefixed endpoint
        .then((response) => {
          const products = response.data;
          if (products.length === 0) {
            console.log("No hay productos disponibles.");
          }
          renderProducts(products);
        })
        .catch((error) => {
          console.error("Error fetching products:", error);
        });
    };

    const fetchProveedores = () => {
        axios
          .get("/proveedor/proveedores") // Correct endpoint
          .then((response) => {
            const proveedores = response.data;
            populateProveedorSelect(proveedores);
          })
          .catch((error) => {
            console.error("Error fetching proveedores:", error);
          });
    };

    const populateProveedorSelect = (proveedores) => {
        const proveedorSelect = document.getElementById('proveedor_id');
        proveedorSelect.innerHTML = ''; // Clear existing options

        proveedores.forEach(proveedor => {
            const option = document.createElement('option');
            option.value = proveedor.id;
            option.textContent = `ID: ${proveedor.id}, Nombre: ${proveedor.nombre}`;
            proveedorSelect.appendChild(option);
        });
    };

    const fetchProductosAlternos = () => {
        axios
          .get("/producto/productos") // Using the prefixed endpoint
          .then((response) => {
            const productos = response.data;
            populateProductoAlternoSelect(productos);
          })
          .catch((error) => {
            console.error("Error fetching productos alternos:", error);
          });
    };

    const populateProductoAlternoSelect = (productos) => {
        const productoAlternoSelect = document.getElementById('producto_alterno_id');
        productoAlternoSelect.innerHTML = ''; // Clear existing options

        productos.forEach(producto => {
            const option = document.createElement('option');
            option.value = producto.id;
            option.textContent = `ID: ${producto.id}, Nombre: ${producto.nombre}`;
            productoAlternoSelect.appendChild(option);
        });
    };
  
    const renderProducts = (products) => {
      productContainer.innerHTML = "";
      products.forEach((product) => {
        const productCard = document.createElement("div");
        productCard.classList.add("product-card");
  
        const productImage = document.createElement("img");
        productImage.src = product.img_src;
        productCard.appendChild(productImage);
  
        const productInfo = document.createElement("div");
        productInfo.classList.add("product-info");
  
        const productName = document.createElement("div");
        productName.classList.add("product-name");
        productName.textContent = product.nombre;
        productInfo.appendChild(productName);
  
        const productPrice = document.createElement("div");
        productPrice.classList.add("product-price");
        const finalPrice = (
          product.precio *
          (1 + product.iva / 100) *
          (1 + product.profit_percentage / 100)
        ).toFixed(2);
        productPrice.textContent = `Precio: $${finalPrice}`;
        productInfo.appendChild(productPrice);
  
        const addToCartButton = document.createElement("button");
        addToCartButton.classList.add("add-to-cart-button", "btn", "btn-primary");
        addToCartButton.textContent = "Añadir al carrito";
        addToCartButton.addEventListener("click", () => addToCart(product));
        productInfo.appendChild(addToCartButton);
  
        productCard.appendChild(productInfo);
        productContainer.appendChild(productCard);
      });
    };
  
    const addToCart = (product) => {
      const existingProduct = cart.find((item) => item.id === product.id);
      if (existingProduct) {
        existingProduct.cantidad += 1;
      } else {
        cart.push({ ...product, cantidad: 1 });
      }
      renderCartItems();
    };
  
    const renderCartItems = () => {
      cartItemsContainer.innerHTML = "";
      cart.forEach((item) => {
        const cartItem = document.createElement("div");
        cartItem.classList.add("cart-item");
  
        const itemName = document.createElement("div");
        itemName.textContent = `${item.nombre} (x${item.cantidad})`;
        cartItem.appendChild(itemName);
  
        const itemPrice = document.createElement("div");
        const finalPrice = (
          item.precio *
          (1 + item.iva / 100) *
          (1 + item.profit_percentage / 100)
        ).toFixed(2);
        itemPrice.textContent = `Precio: $${finalPrice}`;
        cartItem.appendChild(itemPrice);
  
        const removeButton = document.createElement("button");
        removeButton.classList.add("btn", "btn-danger", "btn-sm");
        removeButton.textContent = "Eliminar";
        removeButton.addEventListener("click", () => removeFromCart(item));
        cartItem.appendChild(removeButton);
  
        cartItemsContainer.appendChild(cartItem);
      });
    };
  
    const removeFromCart = (item) => {
      cart = cart.filter((cartItem) => cartItem.id !== item.id);
      renderCartItems();
    };
  
    clearCartButton?.addEventListener("click", () => {
      cart = [];
      renderCartItems();
    });
  
    checkoutButton?.addEventListener("click", () => {
      if (cart.length === 0) {
        alert("El carrito está vacío.");
        return;
      }
  
      axios
        .post("/producto/comprar", { cart }) // Using the prefixed endpoint
        .then((response) => {
          alert("Compra realizada con éxito.");
          cart = [];
          renderCartItems();
        })
        .catch((error) => {
          console.error("Error during checkout:", error);
          alert("Hubo un error al realizar la compra.");
        });
    });
  
    searchInput?.addEventListener("input", (event) => {
      const query = event.target.value.toLowerCase();
      const productCards = document.querySelectorAll(".product-card");
      productCards.forEach((card) => {
        const productName = card
          .querySelector(".product-name")
          .textContent.toLowerCase();
        if (productName.includes(query)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  
    stockForm?.addEventListener("submit", function (event) {
      event.preventDefault();
  
      const formData = new FormData(stockForm);
  
      axios
        .post("/producto/add-stock", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          alert("Producto añadido con éxito.");
          fetchProducts();
        })
        .catch((error) => {
          console.error("Error añadiendo el producto:", error);
          alert("Hubo un error al añadir el producto.");
        });
    });
  
    fetchProducts();
    fetchProveedores();
    fetchProductosAlternos();
});

document.addEventListener("DOMContentLoaded", function () {
    const fetchProducts = () => {
      axios
        .get("/producto/productos")
        .then((response) => {
          const products = response.data;
          renderProducts(products);
        })
        .catch((error) => {
          console.error("Error fetching products:", error);
        });
    };
  
    const renderProducts = (products) => {
      const productContainer = document.getElementById("product-list");
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
        productPrice.textContent = `Precio: $${product.precio}`;
        productInfo.appendChild(productPrice);
  
        const btnContainer = document.createElement("div");
        btnContainer.classList.add("btn-container");
  
        const editButton = document.createElement("button");
        editButton.classList.add("btn", "btn-primary");
        editButton.textContent = "Editar";
        editButton.addEventListener("click", () => openEditModal(product));
        btnContainer.appendChild(editButton);
  
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("btn", "btn-danger");
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener("click", () => deleteProduct(product.id));
        btnContainer.appendChild(deleteButton);
  
        productInfo.appendChild(btnContainer);
        productCard.appendChild(productInfo);
        productContainer.appendChild(productCard);
      });
    };
  
    const openEditModal = (product) => {
      const modal = new bootstrap.Modal(document.getElementById("addStockModal"));
      document.getElementById("addStockModalLabel").textContent = "Editar Producto";
      document.getElementById("nombre").value = product.nombre;
      document.getElementById("descripcion").value = product.descripcion;
      document.getElementById("precio").value = product.precio;
      document.getElementById("existencias").value = product.existencias;
      document.getElementById("min_existencias").value = product.min_existencias;
      document.getElementById("img_src").required = false; // Image is optional for editing
      document.getElementById("proveedor_id").value = product.proveedor_id;
      document.getElementById("producto_alterno_id").value = product.producto_alterno_id;
      document.getElementById("add-stock-form").dataset.editing = product.id;
      modal.show();
    };
  
    const deleteProduct = (productId) => {
      axios
        .delete(`/producto/delete/${productId}`)
        .then((response) => {
          alert("Producto eliminado con éxito.");
          fetchProducts();
        })
        .catch((error) => {
          console.error("Error eliminando el producto:", error);
          alert("Hubo un error al eliminar el producto.");
        });
    };
  
    document.getElementById("add-stock-form").addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(this);
      const isEditing = this.dataset.editing;
  
      if (isEditing) {
        axios
          .put(`/producto/edit/${isEditing}`, formData)
          .then((response) => {
            alert("Producto editado con éxito.");
            fetchProducts();
          })
          .catch((error) => {
            console.error("Error editando el producto:", error);
            alert("Hubo un error al editar el producto.");
          });
      } else {
        axios
          .post("/producto/add-stock", formData)
          .then((response) => {
            alert("Producto añadido con éxito.");
            fetchProducts();
          })
          .catch((error) => {
            console.error("Error añadiendo el producto:", error);
            alert("Hubo un error al añadir el producto.");
          });
      }
    });
  
    fetchProducts();
  });
  
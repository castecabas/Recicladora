document.addEventListener("DOMContentLoaded", () => {
    // Precargar todas las imágenes para que tengamos sus dimensiones
    const preloadImages = () => {
        const images = document.querySelectorAll('.miniature');
        images.forEach(img => {
            // Establecer un evento para cuando la imagen cargue
            img.onload = function() {
                // Cuando la imagen cargue, actualiza la altura del contenedor si está abierto
                const toggleContent = img.closest('.toggle-content');
                if (toggleContent && toggleContent.classList.contains('show')) {
                    toggleContent.style.maxHeight = toggleContent.scrollHeight + "px";
                }
            };
            
            // Si la imagen ya está cargada (desde caché)
            if (img.complete) {
                img.onload();
            }
        });
    };

    // Llamar a precargar imágenes
    preloadImages();

    // Manejar los botones de toggle
    document.querySelectorAll(".toggle-button").forEach(button => {
        button.addEventListener("click", function () {
            const content = this.nextElementSibling;

            // Alternar el contenido actual sin cerrar los otros
            if (content.classList.contains("show")) {
                content.style.maxHeight = null;
                content.classList.remove("show");
            } else {
                // Actualizar la altura después de un pequeño retraso para dar tiempo a que el DOM se actualice
                setTimeout(() => {
                    content.style.maxHeight = content.scrollHeight + "px";
                }, 10);
                content.classList.add("show");
            }
        });
    });
});
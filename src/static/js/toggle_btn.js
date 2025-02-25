document.addEventListener("DOMContentLoaded", () => {
    // Precargar todas las imágenes 
    const preloadImages = () => {
        const images = document.querySelectorAll('.miniature');
        images.forEach(img => {
            // Establecer un evento para cuando la imagen cargue
            img.onload = function() {
                // Cuando la imagen cargue, actualiza la altura del contenedor
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
            
            if (content.classList.contains("show")) {
                content.style.maxHeight = null;
                content.classList.remove("show");
            } else {
                setTimeout(() => {
                    content.style.maxHeight = content.scrollHeight + "px";
                }, 10);
                content.classList.add("show");
            }
        });
    });
});
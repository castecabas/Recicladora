document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toggle-content").forEach(content => {
        // Establece el max-height al cargar la página
        content.style.maxHeight = content.scrollHeight + "px";
    });

    document.querySelectorAll(".toggle-button").forEach(button => {
        button.addEventListener("click", function () {
            const content = this.nextElementSibling;

            if (content.classList.contains("show")) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }

            content.classList.toggle("show");
        });
    });
});
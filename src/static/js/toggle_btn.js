document.addEventListener("DOMContentLoaded", () => {
    
    const preloadImages = () => {
        const images = document.querySelectorAll('.miniature');
        images.forEach(img => {
            img.onload = function() {
                const toggleContent = img.closest('.toggle-content');
                if (toggleContent && toggleContent.classList.contains('show')) {
                    toggleContent.style.maxHeight = toggleContent.scrollHeight + "px";
                }
            };
            
            if (img.complete) {
                img.onload();
            }
        });
    };

    preloadImages();

    document.querySelectorAll(".toggle-button").forEach(button => {
        button.addEventListener("click", function () {
            const content = this.nextElementSibling;

            document.querySelectorAll(".toggle-content.show").forEach(openContent => {
                if (openContent !== content) {
                    openContent.style.maxHeight = null;
                    openContent.classList.remove("show");
                }
            });

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
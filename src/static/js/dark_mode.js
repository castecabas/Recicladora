document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("darkModeToggle");
    const darkModeEnabled = localStorage.getItem("darkMode") === "enabled";

    // Aplicar el modo oscuro si estaba activado
    if (darkModeEnabled) {
        document.body.classList.add("dark-mode");
        toggle.checked = true;
    }

    // Alternar el modo oscuro al cambiar el checkbox
    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            document.body.classList.add("dark-mode");
            localStorage.setItem("darkMode", "enabled");
        } else {
            document.body.classList.remove("dark-mode");
            localStorage.setItem("darkMode", "disabled");
        }
    });
});
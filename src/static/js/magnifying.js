// Funcionalidad de lupa para imágenes
document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que el DOM esté completamente cargado
    setTimeout(function() {
        // Obtener los elementos necesarios
        const imagen = document.getElementById('resultImage');
        const lupa = document.querySelector('.img-magnifier-glass');
        const contenedor = document.querySelector('.img-magnifier-container');
        
        // Verificar que existan todos los elementos
        if (!imagen || !lupa || !contenedor) {
            console.error('Falta uno o más elementos para la lupa.');
            return;
        }
        
        // Nivel de zoom (aumenta o disminuye según necesites)
        const zoom = 2;
        
        // Activar la lupa solo cuando la imagen se haya cargado
        imagen.addEventListener('load', iniciarLupa);
        
        // Función para inicializar la lupa
        function iniciarLupa() {
            // Si la imagen no está cargada o no tiene src, no continuar
            if (!imagen.complete || !imagen.src) {
                return;
            }
            
            // Mostrar la lupa al entrar con el mouse
            contenedor.addEventListener('mouseenter', function() {
                if (imagen.src) {
                    lupa.style.display = 'block';
                }
            });
            
            // Ocultar la lupa al salir con el mouse
            contenedor.addEventListener('mouseleave', function() {
                lupa.style.display = 'none';
            });
            
            // Mover la lupa al mover el mouse
            contenedor.addEventListener('mousemove', moverLupa);
        }
        
        // Función para mover la lupa siguiendo el cursor
        function moverLupa(e) {
            // Obtener la posición del cursor
            let pos = obtenerPosicionCursor(e);
            let x = pos.x;
            let y = pos.y;
            
            // Evitar que la lupa se salga de los límites de la imagen
            let limiteX = imagen.width - (lupa.offsetWidth / zoom);
            let limiteY = imagen.height - (lupa.offsetHeight / zoom);
            
            // Ajustar coordenadas si se exceden los límites
            x = Math.min(Math.max(x, lupa.offsetWidth / zoom), limiteX);
            y = Math.min(Math.max(y, lupa.offsetHeight / zoom), limiteY);
            
            // Posicionar la lupa en el cursor
            lupa.style.left = (x - lupa.offsetWidth / 2) + 'px';
            lupa.style.top = (y - lupa.offsetHeight / 2) + 'px';
            
            // Configurar la imagen ampliada dentro de la lupa
            lupa.style.backgroundImage = "url('" + imagen.src + "')";
            lupa.style.backgroundSize = (imagen.width * zoom) + "px " + (imagen.height * zoom) + "px";
            
            // Calcular la posición del fondo para mostrar la parte correcta ampliada
            let bgPosX = -((x * zoom) - lupa.offsetWidth / 2);
            let bgPosY = -((y * zoom) - lupa.offsetHeight / 2);
            lupa.style.backgroundPosition = bgPosX + "px " + bgPosY + "px";
        }
        
        // Función para obtener la posición exacta del cursor dentro de la imagen
        function obtenerPosicionCursor(e) {
            let rect = imagen.getBoundingClientRect();
            let x = e.pageX - rect.left - window.pageXOffset;
            let y = e.pageY - rect.top - window.pageYOffset;
            return {x: x, y: y};
        }
    }, 100); // Pequeño retraso para asegurar que los elementos están cargados
});
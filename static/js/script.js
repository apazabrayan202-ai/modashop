// Espera a que la pagina cargue completamente
document.addEventListener('DOMContentLoaded', function () {

    const pagina = document.getElementById('pagina-detalle');
    if (!pagina) return;  // Solo se ejecuta en la pagina de detalle

    // --- Leer los datos que Django dejo en los atributos data-* ---
    const tallas = pagina.dataset.tallas.split(',').map(t => t.trim());
    const colores = pagina.dataset.colores.split(',').map(c => c.trim());
    const stock = parseInt(pagina.dataset.stock);
    const productoId = pagina.dataset.productoId;

    let tallaSeleccionada = null;
    let colorSeleccionado = null;
    let cantidad = 1;

    // --- Construir botones de talla ---
    const contTalla = document.getElementById('selector-talla');
    tallas.forEach(talla => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'opcion';
        btn.textContent = talla;
        btn.onclick = function () {
            contTalla.querySelectorAll('.opcion').forEach(b => b.classList.remove('activo'));
            btn.classList.add('activo');
            tallaSeleccionada = talla;
            actualizarBoton();
        };
        contTalla.appendChild(btn);
    });

    // --- Construir botones de color ---
    const contColor = document.getElementById('selector-color');
    colores.forEach(color => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'opcion';
        btn.textContent = color;
        btn.onclick = function () {
            contColor.querySelectorAll('.opcion').forEach(b => b.classList.remove('activo'));
            btn.classList.add('activo');
            colorSeleccionado = color;
            actualizarBoton();
        };
        contColor.appendChild(btn);
    });

    // --- Selector de cantidad ---
    const spanCantidad = document.getElementById('cantidad');
    document.getElementById('btn-menos').onclick = function () {
        if (cantidad > 1) {
            cantidad--;
            spanCantidad.textContent = cantidad;
        }
    };
    document.getElementById('btn-mas').onclick = function () {
        if (cantidad < stock) {
            cantidad++;
            spanCantidad.textContent = cantidad;
        }
    };

    // --- Activar el boton de compra solo cuando todo este seleccionado ---
    function actualizarBoton() {
        const boton = document.getElementById('btn-whatsapp');
        if (tallaSeleccionada && colorSeleccionado) {
            boton.disabled = false;
            boton.textContent = 'COMPRAR POR WHATSAPP';
        }
    }

    // --- Manejar el clic del boton de WhatsApp ---
    const botonWhatsApp = document.getElementById('btn-whatsapp');
    botonWhatsApp.onclick = function () {
        botonWhatsApp.disabled = true;
        botonWhatsApp.textContent = 'Generando enlace...';

        const formData = new FormData();
        formData.append('producto_id', productoId);
        formData.append('talla', tallaSeleccionada);
        formData.append('color', colorSeleccionado);
        formData.append('cantidad', cantidad);

        fetch('/pedido/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                window.open(data.url, '_blank');
                botonWhatsApp.disabled = false;
                botonWhatsApp.textContent = 'COMPRAR POR WHATSAPP';
            } else if (data.error) {
                alert('Error: ' + data.error);
                botonWhatsApp.disabled = false;
                botonWhatsApp.textContent = 'COMPRAR POR WHATSAPP';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al generar el enlace. Intenta de nuevo.');
            botonWhatsApp.disabled = false;
            botonWhatsApp.textContent = 'COMPRAR POR WHATSAPP';
        });
    };

    // --- Obtener el token CSRF de las cookies ---
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return cookie.substring(name.length + 1);
            }
        }
        return '';
    }

});  // ← AQUÍ TERMINA EL DOMContentLoaded


// =============================================
// FUNCIONES GLOBALES (FUERA DEL DOMContentLoaded)
// =============================================

// Cambiar el orden de los productos en la tienda
function cambiarOrden(orden) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('orden', orden);
    window.location.search = urlParams.toString();
}
// ===== Menú hamburguesa para celular =====
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('menu');
    
    if (menuToggle && menu) {
        menuToggle.addEventListener('click', function() {
            menu.classList.toggle('activo');
        });
    }
});
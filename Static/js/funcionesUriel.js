// Funcion para obtener la Cookie y mandarla al Back
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {  
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }}}
    return cookieValue;
}

agregarProducto = (elementoHTML) =>{
    let idComida = elementoHTML.dataset.id;
    let inputComida = document.querySelector("#input-" + idComida);

    let nombre = elementoHTML.dataset.nombre;
    let pedido = parseInt(inputComida.value);   
    let max = parseInt(inputComida.max);
    let precio = parseFloat(inputComida.dataset.precio);

    if(pedido>max){
        alert("No existen tantas unidades de tu comida deseada");
        return;
    }

    agregarCarrito(idComida, nombre, precio, pedido);
}

agregarCarrito = (id, nombre, precio, unidades) =>{

    let pedidos = JSON.parse(localStorage.getItem("pedidos"));

    if(pedidos==null){
        pedidos = {};
    }


    let total = unidades*precio;

    pedidos[id] = {
        unidades: unidades, 
        nombre: nombre,
        precio:precio, 
        total:total 
    };

    localStorage.setItem("pedidos", JSON.stringify(pedidos))
}
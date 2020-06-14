// var server = "https://uaqeats.herokuapp.com"
var server = "127.0.0.1:8000"

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
            }
        }
    }
    return cookieValue;
}


initCarrito = () => {

    let pedidos = JSON.parse(localStorage.getItem("pedidos"));
    let tamañoPedido = Object.keys(pedidos).length;
    checkBotonCompra(tamañoPedido);
    

    let divPedidos = document.querySelector("#pedidos");

    if (pedidos == null|| tamañoPedido==0){
        pedidos = 'No hay productos en tu carrito';
        divPedidos.textContent = pedidos;
        
        return;
    }


    let table = document.createElement("table");
    let tr1 = document.createElement("tr");

    let th1 = document.createElement("th");
    th1.appendChild(document.createTextNode("Nombre"));
    let th2 = document.createElement("th");
    th2.appendChild(document.createTextNode("Precio c/u"));
    let th4 = document.createElement("th");
    th4.appendChild(document.createTextNode("Unidades"));
    let th3 = document.createElement("th");
    th3.appendChild(document.createTextNode("Total"));
    let th5 = document.createElement("th");
    th5.appendChild(document.createTextNode("Eliminar"));
    tr1.appendChild(th1);
    tr1.appendChild(th2);
    tr1.appendChild(th4);
    tr1.appendChild(th3);
    tr1.appendChild(th5);

    table.appendChild(tr1);

    let keys = Object.keys(pedidos);
    let total = 0;
    for (let x = 0; x < Object.keys(pedidos).length; x++) {
        let key = keys[x];
        // console.log(key, ":", pedidos[key]);

        let tr = document.createElement("tr");
        tr.setAttribute('id', pedidos[key]['id']);
        let td1 = document.createElement("td");
        td1.appendChild(document.createTextNode(pedidos[key]['nombre']));

        let td2 = document.createElement("td");
        td2.appendChild(document.createTextNode('$' + pedidos[key]['precio'].toFixed(2)));

        let td4 = document.createElement("td");
        td4.appendChild(document.createTextNode(pedidos[key]['unidades']));

        let td3 = document.createElement("td");
        td3.appendChild(document.createTextNode('$' + pedidos[key]['total'].toFixed(2)));
        total += parseFloat(pedidos[key]['total']);

        let td5 = document.createElement("td");
        let btnDelete = document.createElement("button");
        btnDelete.textContent = 'Eliminar';
        btnDelete.setAttribute('class', 'alguna-clase');
        btnDelete.setAttribute('data-id', pedidos[key]['id']);
        btnDelete.setAttribute('onclick', 'eliminarProducto(this)');
        td5.appendChild(btnDelete);

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td4);
        tr.appendChild(td3);
        tr.appendChild(td5);
        table.appendChild(tr);
    }

    divPedidos.appendChild(table);

    let divTotal = document.createElement('p');
    divTotal.setAttribute('id', 'totalProductos');
    divTotal.appendChild(document.createTextNode("Total: $" + total.toFixed(2)));
    divPedidos.appendChild(divTotal);
}

eliminarProducto = (elementoHTML) =>{
    let pedidos = JSON.parse(localStorage.getItem("pedidos"));
    let idProducto = elementoHTML.dataset.id;
    delete pedidos[idProducto];
    localStorage.setItem("pedidos", JSON.stringify(pedidos));

    let tamañoPedidos = Object.keys(pedidos).length;
    checkBotonCompra(tamañoPedidos);
    // console.log(pedidos)
    // console.log(tamañoPedidos);
    if(tamañoPedidos==0){
        let divPedidos = document.querySelector("#pedidos");
        let pedidos = 'No hay productos en tu carrito';
        divPedidos.textContent = pedidos;
        return;
    }


    let trProducto = document.querySelector(`#${CSS.escape(idProducto)}`);
    let totalProducto = trProducto.cells[3].textContent;
    totalProducto = totalProducto.substring(1, totalProducto.length);
    totalProducto = parseFloat(totalProducto);
    // console.log(totalProducto);

    let totalProductos = document.querySelector('#totalProductos');
    totalProductos = totalProductos.textContent;
    totalProductos = totalProductos.substring(8, totalProductos.length);
    totalProductos = parseFloat(totalProductos);
    // console.log(totalProductos);

    let nuevoTotal = totalProductos - totalProducto;
    document.querySelector('#totalProductos').textContent=`Total: \$${nuevoTotal.toFixed(2)}`;
    trProducto.innerHTML='';

}

agregarProducto = (elementoHTML) => {
    let idComida = elementoHTML.dataset.id;
    let inputComida = document.querySelector("#input-" + idComida);

    let nombre = elementoHTML.dataset.nombre;
    let pedido = parseInt(inputComida.value);
    let max = parseInt(inputComida.max);
    let precio = parseFloat(inputComida.dataset.precio);

    if (pedido > max) {
        alert("No existen tantas unidades de tu comida deseada");
        return;
    }

    agregarCarrito(idComida, nombre, precio, pedido);
    alert('Productos agregados correctamente');

}

agregarCarrito = (id, nombre, precio, unidades) => {

    let pedidos = JSON.parse(localStorage.getItem("pedidos"));

    if (pedidos == null) {
        pedidos = {};
    }


    let total = unidades * precio;

    pedidos[id] = {
        id: id,
        unidades: unidades,
        nombre: nombre,
        precio: precio,
        total: total
    };

    localStorage.setItem("pedidos", JSON.stringify(pedidos));
}

checkBotonCompra = (numeroProductos) =>{
    // alert(numeroProductos);
    try{
        let btnTerminarCompra = document.querySelector('#terminarCompra');
        if(numeroProductos>0){
            btnTerminarCompra.removeAttribute('disabled');
        }else{
            btnTerminarCompra.setAttribute('disabled', 'true');

        }
    }catch(error){
        console.error(error);
    }
}

calcularEfectivo = (elementoHTML) =>{
   
    let pedidos = JSON.parse(localStorage.getItem("pedidos"));
    let keys = Object.keys(pedidos);
    let total = 0;

    for (let x = 0; x < Object.keys(pedidos).length; x++) {
        let key = keys[x];
        total += parseFloat(pedidos[key]['total']);
    }

    let creditos = elementoHTML.value;
    let efectivo = document.getElementById('iptEfectivo');

    efectivo.value=total-creditos;
}

pagar = () => {
    let pedidos = JSON.parse(localStorage.getItem("pedidos"));
    let keys = Object.keys(pedidos);
    let total = 0;

    for (let x = 0; x < Object.keys(pedidos).length; x++) {
        let key = keys[x];
        total += parseFloat(pedidos[key]['total']);
    }

    let pago = 0;
    let cbox1 = document.getElementById("cbox1").checked;
    let cbox2 = document.getElementById("cbox2").checked;
    let efectivo = document.getElementById('iptEfectivo').value;
    let creditos = document.getElementById('iptCreditos').value;

    if(cbox1){
        pago+=efectivo;
    }

    if(cbox2){
        pago+=creditos;
    }

    if(total>pago){
        alert('Debes seleccionar otro metodo de pago para completar tu pedido');
    }else{

        // AQUI DEBERIA IR EL AJAX PARA CREAR EL PEDIDO EN LA BASE DE DATOS
        fetch("/store/crearPedido", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept":'application/json',
            'X-Requested-With':"XMLHttpRequest"
        },
        body: JSON.stringify({'pedidos':pedidos, 'total':total, 'pago':efectivo}),
        mode: 'cors',
        cache: 'default',
        credentials: 'include'
        })
        .then(
            respuesta => {
                respuesta.text().then(
                    function(data){
                        console.log(data);
                    }
                )
            }
        )

        alert("Tu pedido ha sido creado. Seras redireccionado a tus pedidos");
        localStorage.setItem('pedidos', '{}');
        window.location='/store/pedidos';
    }



}
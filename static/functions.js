function change_input(event) {
    // Get all radios and check their value. Depending on it, show different input boxes.
    radio = event.srcElement;
    if (radio.value == 'pick_up')
    {
        document.getElementById('address').style.display = 'none';
        document.getElementById('table').style.display = 'none';
        document.getElementById('email').disabled = false
    }
    else if (radio.value == 'on_place')
    {
        document.getElementById('address').style.display = 'none';
        document.getElementById('table').style.display = 'block';
        document.getElementById('email').value = ''
        document.getElementById('email').disabled = true
    }
    else if (radio.value == 'delivery')
    {
        document.getElementById('address').style.display = 'block';
        document.getElementById('table').style.display = 'none';
        document.getElementById('email').disabled = false
    }
    
}

function add_combo() {
    master_div = document.getElementById('order_div');
    order_div = document.createElement('div');
    master_div.appendChild(order_div);

    menu = document.getElementsByName('menu');

    selector = document.createElement('select');
    selector.name = 'combo';
    selector.className = 'buttons'
    order_div.appendChild(selector);

    remove = document.createElement('button');
    remove.setAttribute('type', 'button');
    remove.setAttribute('onclick', 'remove_combo(event)');
    remove.innerHTML = '&#10060';
    order_div.appendChild(remove);

    br = document.createElement('br');
    order_div.appendChild(br);

    for (var i = 0, n = menu.length; i < n; i++) {
        menu_value = menu[i].value
        option = document.createElement('option');
        option.value = menu_value;
        option.innerHTML = 'Combo ' + menu_value;
        selector.appendChild(option);
    }
}

function remove_combo(event) {
    button = event.srcElement;
    buttonParent = button.parentNode;
    buttonParent.remove();
}
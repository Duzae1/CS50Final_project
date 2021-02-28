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
    order_div = document.getElementById('order_div')
    menu = document.getElementsByName('menu')

    selector = document.createElement('select')
    selector.name = 'combo'
}
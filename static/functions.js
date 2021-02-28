function change_input(event) {
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
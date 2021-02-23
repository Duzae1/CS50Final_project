function change_input() {
    if (document.getElementById('delivery').checked == true)
    {
        document.getElementById('address').style.display = 'block';
        document.getElementById('table').style.display = 'none';
    } 
    else
    {
        document.getElementById('address').style.display = 'none';
        document.getElementById('table').style.display = 'block';
    }
}
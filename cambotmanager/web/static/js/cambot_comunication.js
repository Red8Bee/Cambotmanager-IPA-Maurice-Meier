function on_page_loaded(){
    get_status();
    get_items();
    console.log("aaaaaaaaaaaaaaaaa")
}


function reset_click(){
    reset_cambot();
}



// api calls
async function reset_cambot() {

    const request = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/status/reset";
   request.open("POST", url)
   request.send();
   request.onload = () => {
    if(request.status == 200){
        response = JSON.parse(request.response);
        document.getElementById('status').innerHTML = response['robot_status']
    }
    else{
        console.log("errör");
    }
   }
}

async function get_status() {
    const request = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/status";
   request.open("GET", url)
   request.send();
   request.onload = () => {
    if(request.status == 200){
        response = JSON.parse(request.response);
        document.getElementById('status').innerHTML = response['robot_status']
    }
    else{
        console.log("errör");
    }
   }
}

async function get_items(){
    const request = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/inventory";
   request.open("GET", url)
   request.send();
   request.onload = () => {
    if(request.status == 200){
        response = JSON.parse(request.response);
        let innerHTML = ""
        response.forEach(element => {
            innerHTML += '<li class="inventory_item"><div><a>'+element+'</a><button id='+element+'>Download</button></div></li>';
            document.getElementById('inventory').innerHTML = innerHTML;
        });
        response.forEach(element => {
            document.getElementById(element).onclick = function() {
                download_item(element);
            }
        })
    }
    else{
        console.log("errör");
    }
   }
}

async function download_item(id_tag){
    const request = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/inventory/"+id_tag+"/zip";
    window.open(url);
}

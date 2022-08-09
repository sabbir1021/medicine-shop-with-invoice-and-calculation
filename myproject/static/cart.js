// cart js

var updatebtns = document.getElementsByClassName('update-cart')
for (var i=0; i < updatebtns.length; i++) {
    updatebtns[i].addEventListener('click', function(){
        var productId = this.dataset.product 
        var action = this.dataset.action
        var user = this.dataset.user
        console.log('productId:',productId,'Action:',action)
        console.log('User:',user)
        if(user === "AnonymousUser"){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId,action){
    console.log('user is logged in, send data..')
    var url = '/update_item/'
    
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie("csrftoken")
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('date:', data)
        location.reload()
    })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;}

// cart js end


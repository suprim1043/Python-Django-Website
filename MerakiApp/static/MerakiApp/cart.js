var user = '{{request.user}}'
var updatebtn = document.getElementsByClassName("update-cart")
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getToken('csrftoken');

for (var i = 0; i < updatebtn.length; i++) {
    updatebtn[i].addEventListener('click', function () {
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:', productid, "action:", action)
        console.log(user)
        if (user === 'AnonymousUser') {
            addCookieItem(productid, action)
        }
        else {
            updateUserOrder(productid, action)
        }
    })

}


function addCookieItem(productid, action) {
    console.log("Not Logged In")
    if (action == "add") {
        if (cart[productid] == undefined) {
            cart[productid] = { 'quantity': 1 }
        }
        else {
            cart[productid]['quantity'] += 1

        }
        location.reload()
    }



    if (action == "remove") {
        cart[productid]['quantity'] -= 1

        if (cart[productid]['quantity'] <= 0) {
            console.log("remove item")
            delete cart[productid]
        }
        location.reload()
    }


    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}


function updateUserOrder(productid, action) {
    console.log("Logged In")
    var url = '/updateitem'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productid': productid, 'action': action })
    })

        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}


function getCookie(name) {
    var cookieArr = document.cookie.split(";");

    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

var cart = JSON.parse(getCookie('cart'))
console.log('Cart', cart)

if (cart == undefined) {
    cart = {}
    console.log("Cart Was Created", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}





var updatebtn = document.getElementsByClassName("update-cart")
var user = '{{request.user}}'
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
        var quantity = document.getElementById("input-quantity").value
        console.log(quantity)
        var action = this.dataset.action
        console.log('productid:', productid, "action:", action)
        console.log(user)
        if (user === 'AnonymousUser') {
            console.log("Not Logged In")
        }
        else {
            updateUserOrder(productid, action)
        }
    })

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
        })
}
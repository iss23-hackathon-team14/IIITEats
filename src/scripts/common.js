// JS functions and utilities common to multiple files are here

const ORDERS_URL = "/api/orders";
const ORDERS_URL_GET = `${ORDERS_URL}?`;

function post_obj_orders(obj) {
    fetch(ORDERS_URL, {
        method: 'POST',
        body: JSON.stringify(obj),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    })
        .then(response => response.json())
        .then(json => {
            console.log(json);
        });
}

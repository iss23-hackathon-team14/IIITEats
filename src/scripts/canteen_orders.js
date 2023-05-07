const container = document.getElementById("order-container");

const init_text = `
<div style="font-size: 2rem; color: brown">
There are no active orders on this canteen!
</div>
`;

function get_canteen_orders() {
    let url = ORDERS_URL_GET + new URLSearchParams({ action: parseInt(canteen_id) });
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length == 0) {
                container.innerHTML = init_text;
            }
            else {
                container.innerHTML = "";
                for (record of data) {
                    let dest_name = locations[record['order_dest_id']];
                    container.innerHTML += `
                    <div class="order-card" style="position:relative; top:2rem; right:10rem;">
                        <h2>${dest_name}</h2>
                        <p>${record.order_dest_info}</p>
                        <p>Price: <span class="price">Rs ${record.order_cost}</span></p>
                        <button id="accept" class="accept-btn" value='${record.order_id}'>
                            Accept Order
                        </button>
                    </div>
                    `
                }
            }
        });
}

get_canteen_orders().then(function () {
    var buttons = document.querySelectorAll(".accept-btn");
    console.log(buttons)
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function () {
            console.log("hi")
            accept_order(parseInt(buttons[i].value));
        });
    }
});


function accept_order(order_id) {
    console.log(order_id)
    post_obj_orders({ action: 'accept', order_id: order_id }).then(function () { 
        location.href = "/orders.html"; }
    )
}


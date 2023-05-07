const container = document.getElementById("container");

const init_text = `
<div style="font-size: 2rem; color: brown">
You don't have any active orders!
</div>
`;

function get_orders(kind) {
    let url = ORDERS_URL_GET + new URLSearchParams({ action: kind });
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length == 0) {
                container.innerHTML = init_text;
            }
            else {
                container.innerHTML = "";
                for (record of data) {
                    let canteen = canteens[record.order_canteen_id]

                    let items = JSON.parse(record.order_items);
                    let items_str = ""
                    for (const [item_id, num] of Object.entries(items)) {
                        if (num) {
                            let item = canteen.menu[item_id];
                            items_str += `
                                &nbsp;&nbsp;&nbsp;
                                ${item.name} - ₹${item.cost} x ${num} = ₹${item.cost * num}
                                <br>
                            `;
                        }
                    }

                    let dest_name = locations[record.order_dest_id];

                    let delivery_info = "";
                    if (kind == "placer") {
                    
                        if (record.order_deliverer_id) {
                            delivery_info = `
                                <hr class="receipt-line" />
                                <p class="f">
                                    Deliverer Name: <span>${record.order_deliverer_name}</span>
                                </p>
                                <p class="f">
                                    Deliverer Phone: <span>${record.order_deliverer_id}</span>
                                </p>
                            `;
                        }
                    }
                    else {
                        if (record.order_placer_id) {
                            delivery_info = `
                                <hr class="receipt-line" />
                                <p class="f">
                                    Recipient Name: <span>${record.order_placer_name}</span>
                                </p>
                                <p class="f">
                                    Recipient Phone: <span>${record.order_placer_id}</span>
                                </p>
                            `;
                        }
                    }

                    let extra_buttons = "";
                    let status = `<span class="price">Unknown</span>`;
                    if (record.order_status == 'placed') {
                        status = `<span class="price" style="color: green">Order placed</span>`;
                        extra_buttons += `
                            <button class="order_button cancel_order_button" value=${record.order_id}>
                                Cancel Order
                            </button>`;
                    }
                    else {
                        if (record.order_status == 'accepted') {
                            status = `<span class="price" style="color: green">Order accepted</span>`;
                            if (kind == "deliverer") {
                                extra_buttons += `
                                    <button class="order_button cancel_order_button" value=${record.order_id}>
                                        Cancel Order
                                    </button>
                                    <button class="order_button indelivery_button" value=${record.order_id}>
                                        In Delivery
                                    </button>`;
                            }
                        }
                        else if (record.order_status == 'cancelled') {
                            status = `<span class="price" style="color: red">Order cancelled</span>`;
                        }
                        else if (record.order_status == 'indelivery') {
                            status = `<span class="price" style="color: yellow">Order on the way</span>`;
                            if (kind == "deliverer") {
                                extra_buttons += `
                                    <button class="order_button delivered_button" value=${record.order_id}>
                                        Delivered
                                    </button>`;
                            }
                        }
                        else if (record.order_status == 'delivered') {
                            status = `<span class="price" style="color: green">Order delivered</span>`;
                        }
                    }

                    container.innerHTML += `
                    <div class="order-card">
                        <h2>${canteen.name}</h2>
                        <hr class="receipt-line" />
                        <p class="f">Landmark: <span>${dest_name}</span></p>
                        <p class="f">Location: <span>${record.order_dest_info}</span></p>
                        <hr class="receipt-line" />
                        <p class="f">Date: <span>${record.order_date}</span></p>
                        <p class="f">Time: <span>${record.order_time}</span></p>
                        <hr class="receipt-line" />
                        <p class="f">Items: <br>${items_str}</p>
                        <p class="f">Total price: 
                            <span>&#x20B9;${record.order_cost}</span>
                            <span>(including delivery fee)</span>
                        </p>
                        ${delivery_info}
                        <hr class="receipt-line" />
                        <div class="status_bottom">
                            <p>Status: ${status}</p>
                            ${extra_buttons}
                        </div>
                    </div>
                    `
                }
            }
        });
}
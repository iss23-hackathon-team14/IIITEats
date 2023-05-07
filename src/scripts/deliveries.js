

get_orders("deliverer").then(function () {
    const ids = {
        cancel: ".cancel_order_button",
        indelivery: ".indelivery_button",
        delivered: ".delivered_button"
    };

    for (const [kind, id] of Object.entries(ids)) {
        var buttons = document.querySelectorAll(id);
        console.log(buttons)
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener("click", function (event) {
                update_order(kind, parseInt(event.target.value));
            });
        }
    }
});


function update_order(kind, order_id) {
    console.log(order_id)
    post_obj_orders({ action: kind, order_id: order_id }).then(function () {
        location.href = "/deliveries.html";
    }
    )
}
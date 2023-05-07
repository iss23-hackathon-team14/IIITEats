

get_orders("placer").then(function () {
    var buttons = document.querySelectorAll(".cancel_order_button");
    console.log(buttons)
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function () {
            cancel_order(parseInt(buttons[i].value));
        });
    }
});


function cancel_order(order_id) {
    console.log(order_id)
    post_obj_orders({ action: 'cancel', order_id: order_id }).then(function () {
        location.href = "/orders.html";
    }
    )
}


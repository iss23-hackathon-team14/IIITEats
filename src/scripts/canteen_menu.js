const lang = document.getElementById("lang");
const input = document.getElementById("input");

const delivery_charge = 30;

let items_dict = {}

let total_cost = delivery_charge;

function menu_plus(item_id) {
    if (item_id in items_dict) {
        items_dict[item_id]++;
    }
    else {
        items_dict[item_id] = 1;
    }
    document.getElementById(`counter-${item_id}`).innerHTML = items_dict[item_id];
    update_total_cost();
}

function menu_minus(item_id) {
    if (item_id in items_dict) {
        if (items_dict[item_id] >= 1) {
            items_dict[item_id]--;
        }
        document.getElementById(`counter-${item_id}`).innerHTML = items_dict[item_id];
    }
    update_total_cost();
}

function update_total_cost() {
    total_cost = delivery_charge;
    for (const [key, value] of Object.entries(items_dict)) {
        total_cost += items[key]["cost"] * value;
    }
    document.getElementById('order-total').innerHTML = `Order Total: ₹${total_cost}`;
}

function place_order() {
    if (total_cost <= delivery_charge) {
        alert("Could not place order! No items were selected.");
        return;
    }

    let dest_id = parseInt(lang.value);
    if (!dest_id) {
        alert("Could not place order! Select a landmark for the destination.");
        return;
    }

    let dest_info = input.value;
    if (!dest_info) {
        alert("Could not place order! Enter destination info");
        return;
    }

    post_obj_orders({
        action: 'place',
        canteen_id: canteen_id,
        items: JSON.stringify(items_dict),
        dest_id: dest_id,
        dest_info: dest_info,
        cost: total_cost,
    }).then(function () { 
        location.href = "/orders.html" 
    });

}

update_total_cost();

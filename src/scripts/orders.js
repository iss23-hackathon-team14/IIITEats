const ORDERS_URL = "/api/orders";

function place_order(canteen_id, items, dest_id, dest_info) {
    post_obj_to_url({
        action: 'place',
        canteen_id: canteen_id, 
        items: JSON.stringify(items), 
        dest_id: dest_id, 
        dest_info: dest_info,
    }, ORDERS_URL);
}
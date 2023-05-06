// JS functions and utilities common to multiple files are here

function post_obj_to_url(obj, url) {
    fetch(url, {
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

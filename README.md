# IIITEats

We are a decentralized freelancing-style delivery solution for the IIIT community to simplify intra-campus deliveries while making some money off of it.


## Features

### Canteens/Home Page 

- Displays the various canteens available on campus and allows the user to choose the canteen they want to order from. 
- Clicking on a certain canteen will prompt you with a login/signup form (the first time you click on any canteen while on the website). You are then taken to the order page of that canteen where you can enter the landmark and location from where you want to pick your food up as well as adding items to your order.
- The final cost of your order is displayed at the bottom of the page. The user can finally click on the place order button to place their order, after which they are redirected to the "Orders" page to view their current (and also past) orders.
- Additionally, the user can click on the "View Placed Orders" button to view any available orders on this canteen, if any, so that they can deliver an order. On accepting an order, you will be redirected to the Deliveries page which shows a record of your deliveries.

### Orders page

- On placing your order or on clicking on "Orders" in the navbar, you will be redirected to the orders page where you will be able to view the status of your current orders as well as your past orders. 
- You will also have the option to cancel the order if it has not been accepted yet.

### Deliveries page

- On accepting an order from the Accept Orders page, you will be redirected to the Deliveries page, where you will be able to view the entire order, location to deliver the order, as well as the contact details of the user to deliver to.
- Additionally, there are buttons to change the status of the delivery. These status changes will be displayed in the current orders in the orders page from the user who ordered the food and the status will be changed when the user delivering the food with the status buttons.

### About page

- Has information about the team members, purpose and convenience of the website.

## Frameworks/Packages
We used `Flask` as a server, and the python standard library module `sqlite3` as SQL DBMS.


## Running the project

Make sure you have Python and Flask installed.

Just launch `app.py` with python at the base directory of the project. It should fire up a HTTP server on localhost.


## Contributions

### Bhavani

- Worked on the front end for the Canteen pages, Accept Orders, and Deliveries pages. 
- Made the About page as well as populated the database containing the food items of various canteens.

### Faisal

- Made navbar, footer, logo and structured the layout around it.
- Worked on the front end for Canteens pages.
- Made login/register pages.

### Ankith

- Made backend for everything.
- Worked on most of the JS code for frontend.

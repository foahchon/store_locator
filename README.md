# Store Locator API

 The idea of this API is to allow members to sign, associate vendors with themselves, associate products with their vendors, and then allow the vendors to add themselves or their products to the stores. This way, a store can have products from many vendors. Such an API could be used for a website that allows potential consumers to find niche products sold in their local area.

 ## Getting started

 The steps to setup and run this API locally are as follows:

 1. Unzip the contents of `store_locator.zip` file.
 2. In your PostgreSQL database, create a database called something like `store_locator`.
 3. Modify the `SQLALCHEMY_DATABSE_URI` constant on line 9 of `\flask\store_locator\src\__init__.py` to point to your own local PostgreSQL database.
 4. In the root folder where `store_locator` was unzipped, create a virtual environment with something like the following command: `python -m venv venv`. Once it's created, activate it (this will vary depending on your operating system; on Windows it's `./venv/scripts/activate`).
 5. Once inside the Python virtual environment, install the requirements listed in the `requirements.txt` file: `python -m pip install -r requirements.txt`.
 6. Navigate to the `\flask\store_locator` folder and run: `flask db upgrade` to recreate the database schema in your local PostgreSQL database.
 7. Once the above command is finished, type `flask run` to start the application.

## API Endpoints

### Members
The members section of the API deals primarily with registering members, and allowing for CRUD operations on members' profiles.

`/members` **[POST]**  
Creates a member profile according to the parameters specified. Returns profile created including newly created ID.  
_Required fields:_ `name`, `email`, `password`.

`/members` **[GET]**  
Returns a list of all registered members on the site, including their names, emails, and ID's.

`/members/<member_id>` **[GET]**  
Will show detailed information for just one member.

`/members/<member_id>` **[PATCH, UPDATE]**  
Updates a member's profile according to the data included in the JSON request. The member's password must be supplied.

`/members/<member_id>` **[DELETE]**  
Deletes a member's profile.

`/members/<member_id>/vendors` **[GET]**  
Returns a list of vendors associated with the specified member's profile.

### Vendors
The vendors section of the API deals with performing CRUD operations on vendors' profiles, along with listing what stores a given vendor is associated with.

`/vendors` **[POST]**  
Creates a vendor's profile. Name, address, and owning member's ID must all be supplied.  
_Required fields:_ `name`, `street_address`, `city`, `state`, `zip_code`, `member_id`

`/vendors` **[GET]**  
Returns a list of exisiting vendors along with detailed data on each.

`/vendors/<vendor_id>` **[GET]**  
Retruns detailed information on the specified vendor.

`/vendors/<vendor_id>` **[PATCH, UPDATE]**  
Updates a vendor's profile according to the data included in the JSON request.

`/vendors/<vendor_id>` **[DELETE]**  
Deletes a vendor's profile.

`/vendors/<vendor_id>/stores` **[GET]**  
Returns a list of stores associated with a given vendor. This is a list of stores where a vendor's products are sold.

### Products
The products section of the API deals with performing CRUD operations on various products, adding them to vendors, and associating them with stores. Products are associated with stores separately from vendors, since not all of a vendor's products must be sold at a given store.

`/products` **[POST]**  
Creates a product. Once a product has been created, its `vendor_id` cannot be updated.
_Required fields:_ `name`, `description`, `price`, `vendor_id`

`/products` **[GET]**  
Returns a detailed list of all products.

`/products/<product_id>` **[GET]**  
Returns detailed information about a specific product.

`/products/<product_id>` **[PATCH, UPDATE]**  
Updates a product's information according to the data included in the JSON request. A product's `vendor_id` cannot not be updated.

`/products/<product_id>` **[DELETE]**  
Deletes a product.

`/products/<product_id>/stores` **[GET]**  
Gets a list of stores associated with a product. This would be a list of stores where the product is sold.

### Stores
The stores section of the API deals with performing CRUD operations on stores, as well as finding vendors who sell their products at specified stores, or finding products sold at those stores.

`/stores` **[POST]**  
Creates a store.  
_Required fields:_ `name`, `street_address`, `city`, `state`, `zip_code`, `latitude`, `longitude`.

`/stores` **[GET]**  
Returns a detailed list of all stores.

`/stores/<store_id>` **[GET]**  
Returns detailed information about a specific store.

`/stores/<store_id>` **[PATCH, UPDATE]**  
Updates a store's information according to the data included in the JSON request.

`/stores/<store_id>` **[DELETE]**  
Deletes a store.

`/stores/<store_id>/products/<product_id>` **[POST, DELETE]**  
Adds or removes a product to/from a given store. If the method used is `POST`, the product is added to the store; if `DELETE` is used, the store is removed. A product cannot be added to a store unless the product's vendor is added to the store first.

`/stores/<store_id>/vendors/<vendor_id>` **[POST, DELETE]**  
Adds or removes a vendor to/from a given store. If the method used is `POST`, the vendor is added to the store; if `DELETE` is used, the vendor is removed. If a vendor is removed from a store, all of that vendor's products will be removed as well.

## Retrospective

### How did the project evolve over time?
I had originally conceived of an API that simply allowed vendors to list and update their products, and perhaps inventory levels. When I learned that PostGIS existed, the idea for a sort of universal, or niche-product locator occurred to me. As it stands, the API stores a store's geocoordinates, but doesn't use them, yet.

I also initially thought I was going to use raw SQL for this project, but before too long I decided that it was too much code to write by hand that was also error-prone and tedious. ORM's exists to solve exactly this problem, so I decided to make use of them.

### Did you choose to use an ORM or raw SQL? Why?
I decided to use an ORM because interacting with a database is much simpler and requires far less tedious and error-prone code than translating requests to SQL queries, dispatching them to the database, getting the data back, and packaging it back into objects that can be used by the application. An ORM takes care of a lot of that busy work.

### What future improvements are in store, if any?
I'd like to implement a proximity-based search whereby the user could specify their location, along with a product they're looking to buy, and see what nearby stores sell those products. Optionally, a user could also see where a vendor's products are sold nearby. This would probably involve some combination of using an extension like PostGIS and a map display widget like Google Maps. Some of the ORM code could probably also be improved so that it results in more efficient quieries. If this were to be used in a real-world app, a fully-functional user system would also be necessary.
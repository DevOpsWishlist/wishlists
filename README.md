# wishlists
A collection of lists of item products I wish I had


These are the RESTful routes for `wishlists` and `items`
```
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /

list_wishlists     GET      /wishlists
create_wishlists   POST     /wishlists
get_wishlists      GET      /wishlists/<wishlist_id>
update_wishlists   PUT      /wishlists/<wishlist_id>
delete_wishlists   DELETE   /wishlists/<wishlist_id>

list_items    GET      /wishlists/<int:wishlist_id>/items
create_items  POST     /wishlists/<wishlist_id>/items
get_items     GET      /wishlists/<wishlist_id>/items/<item_id>
update_items  PUT      /wishlists/<wishlist_id>/items/<item_id>
delete_items  DELETE   /wishlists/<wishlist_id>/items/<item_id>
```


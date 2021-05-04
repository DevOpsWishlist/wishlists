Feature: The wishlist service back-end
    As a customer
    I need a RESTful catalog service
    So that I can keep track of all my wishlists and items within

Background:
    Given the following wishlists
        |  name | items | category |
        |  books         | 1              | school            |
        |  food          | 1              | grocery           |
        |  default       | 2              | other             |
      
    # Given the following items
    #     | item_id | wishlist_id | item_price      | item_name |  
    #     |       1 | 1           | 1               | cs        | 
    #     |       2 | 1           | 2               | math      | 
    #     |       3 | 3           | 1               | art       | 
    #     |       4 | 2           | 3               | burger    | 

Scenario: The server is running
    When I visit the "home page"
    Then I should see "WISHLIST RESTful Service" in the title
    And I should not see "404 Not Found"

####################
# CRUD WISHLISTS
####################
Scenario: Create a wishlist 
    When I visit the "home page"
    #And I set the "Wishlist ID" to "test"
    And I set the "Category" to "school"
    And I press the "Create" button
    Then I should see the message "Success"
    

Scenario: List all wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "food" in the results
    And I should see "books" in the results
    And I should not see "clothes" in the results

Scenario: Update a wishlist
    When I visit the "Home Page"
    And I set the "Name" to "books"
    And I press the "Search" button
    Then I should see "books" in the "Name" field
    Then I should not see "food" in the results
    When I change "Name" to "clothes"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "clothes" in the results
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "clothes" in the results
    Then I should not see "books" in the results

Scenario: Delete a wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "books" in the "Wishlist Name" field
    And I should see "food" in the "Wishlist Name" field
    And I should not see "clothes" in the results
    When I select "1" in the "Wishlist ID" field
    And I press the "Delete" button 
    Then I should not see "books" in the results 
    Then I should see "food" in the results 

####################
# CRUD ITEMS
####################

Scenario: Create a item
    When I visit the "Home Page"
    And I set the "Item Name" to "test"
    And I set the "Item ID" to "5"
    And I set the "Item Wishlist ID" to "4"
    And I set the "Item Price" to "2"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: List all items
    When I visit the "Home Page"
    And I set the "Wishlist Id" to "1"
    And I press the "Search" button
    Then I should see "cs" in the results
    And I should not see "burger" in the results

Scenario: Update an Item 
    When I visit the "Home Page"
    And I set the "Item Name" to "math"
    And I press the "Search" button
    Then I should see "math" in the "Item Name" field
    And I should see "burger" in the "IItem Name" field
    When I change "Item Name" to "physics"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear" button
    And I paste the "Item Id" field
    And I press the "Retrieve" button
    Then I should see "physics" in the "Item Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "physics" in the results
    Then I should not see "math" in the results

Scenario: Delete an item
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "math" in the "Item Name" field
    And I should see "cs" in the "Item Name" field
    And I should not see "physics" in the results
    When I select "1" in the "Item ID" field
    And I press the "Delete" button 
    Then I should not see "cs" in the results 
    Then I should see "math" in the results 

####################
# QUERY ACTION WISHLISTS
####################



####################
# QUERY ACTION ITEMS
####################

Feature: The pet store service back-end
    As a customer
    I need a RESTful catalog service
    So that I can keep track of all my wishlists and items within

Background:
    Given the following wishlists
        | wishlist id | wishlist name | customer id |
        |           1 | books         | 1           |
        |           2 | food          | 1           |
        |           3 | default       | 2           |
    Given the following items
        | item id | item wishlist id | item price      | item  name |  
        |       1 | 1                | 1               | cs        | 
        |       2 | 1                | 2               | math      | 
        |       3 | 3                | 1               | art       | 
        |       4 | 2                | 3               | burger    | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "wishlist RESTful Service" in the title
    And I should not see "404 Not Found"

####################
# CRUD WISHLISTS
####################
Scenario: Create a wishlist 
    When I visit the "Home Page"
    And I set the "Wishlist ID" to "test"
    And I set the "Customer ID" to "1"
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
    And I set the "Wishlist Name" to "books"
    And I press the "Search" button
    Then I should see "books" in the "Wishlist Name" field
    And I should see "food" in the "Wishlist Name" field
    When I change "Wishlist Name" to "clothes"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    And I paste the "Wishlist Id" field
    And I press the "Retrieve" button
    Then I should see "clothes" in the "Wishlist Name" field
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

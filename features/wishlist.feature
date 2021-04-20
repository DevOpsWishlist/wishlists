Feature: The pet store service back-end
    As a customer
    I need a RESTful catalog service
    So that I can keep track of all my wishlists and items within

Background:
    Given the following wishlists
        | wishlist_id | wishlist_name | customer_id |
        |           1 | books         | 1           |
        |           2 | food          | 1           |
        |           3 | default       | 2           |
    Given the following items
        | item_id | item_wishlist_id | item_price      | item_name |  
        |       1 | 1                | 1               | cs        | 
        |       2 | 1                | 2               | math      | 
        |       3 | 3                | 1               | cs        | 
        |       4 | 2                | 3               | burger    | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "wishlist RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a wishlist
    When I visit the "Home Page"
    And I set the "wishlist" to "test"
    And I set the "customer_id" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    

Scenario: List all wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "food" in the results
    And I should see "books" in the results
    And I should not see "clothes" in the results


Scenario: Create a item
    When I visit the "Home Page"
    And I set the "item_name" to "test"
    And I set the "item_id" to "5"
    And I set the "item_wishlist_id" to "4"
    And I set the "item_price" to "2"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: List all items
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "Search" button
    Then I should see "cs" in the results
    And I should not see "burger" in the results

Scenario: Update a wishlist
    When I visit the "Home Page"
    And I set the "wishlist_name" to "books"
    And I press the "Search" button
    Then I should see "books" in the "wishlist_name" field
    And I should see "food" in the "wishlist_name" field
    When I change "wishlist_name" to "clothes"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "clothes" in the "wishlist_name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "clothes" in the results
    Then I should not see "books" in the results

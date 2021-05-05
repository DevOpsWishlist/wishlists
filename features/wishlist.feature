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
      
Scenario: The server is running
    When I visit the "home page"
    Then I should see "WISHLIST RESTful Service" in the title
    And I should not see "404 Not Found"

####################
# CRUD WISHLISTS
####################
Scenario: Create a wishlist 
    When I visit the "home page"
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

    #ID field not populating 
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
    Then I should see "books" in the "Name" field
    And I should see "food" in the results
    And I should not see "clothes" in the results

    #broken here - don't kknow how to get the ID for the testing
    When I select "1" in the "ID" field 
   
    And I press the "Delete" button 
    Then I should not see "books" in the results 
    Then I should see "food" in the results 

####################
# QUERY ACTION WISHLISTS
####################

Scenario: Query Wishlists by Category
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "category" to "school"
    And I press the "Search" button
    Then I should see "school" in the results
    Then I should not see "clothes" in the results
    And I should not see "other" in the results 

Scenario: Query Wishlists by Name
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "name" to "food"
    And I press the "Search" button
    Then I should see "food" in the results
    And I should see "grocery" in the results
    Then I should not see "clothes" in the results
    And I should not see "other" in the results 

Feature: The shopcarts service back-end
    As an E-Commerce Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts


Background:
    Given the following shopcarts
        | shopcart_id | name       | email              | phone_number    | date_joined    |
        | 1           | Chris      | chris@gmail.com    | 7575550000      | 2015-05-02     |
        | 2           | Katelyn    | kate@gmail.com     | 5835550987      | 2006-05-05     |
        | 3           | Jon        | john@gmail.com     | 2095558739      | 2023-01-20     |
        | 4           | Steven     | steven@gmail.com   | 2098675535      | 2005-05-20     |


    Given the following items
        | shopcart_email         | name       | quantity  | color     | size  | price |
        | chris@gmail.com        | shirt      | 1         | red       | M     | 20.00 |
        | chris@gmail.com        | pants      | 2         | blue      | S     | 30.00 |
        | kate@gmail.com         | pants      | 1         | black     | L     | 25.00 |
        | kate@gmail.com         | shirt      | 1         | green     | M     | 20.00 |
        | john@gmail.com         | underwear  | 3         | white     | L     | 15.00 |
        | steven@gmail.com       | headband   | 1         | yellow    | NA    | 5.00  |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart Demo RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the "Name" to "Greg"
    And I set the "Email" to "greg@test.com"
    And I set the "Phone Number" to "6786286400"
    And I set the "Date Joined" to "04/12/2023"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Greg" in the "Name" field
    And I should see "greg@test.com" in the "Email" field
    And I should see "6786286400" in the "Phone Number" field
    And I should see "2023-04-12" in the "Date Joined" field

Scenario: List all shopcarts
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Chris" in the results
    And I should see "Steven" in the results
    And I should not see "Christiana" in the results

Scenario: Search for name
    When I visit the "Home Page"
    And I set the "Name" to "Chris"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Chris" in the results
    And I should not see "Katelyn" in the results
    And I should not see "Jon" in the results
    And I should not see "Steven" in the results

Scenario: Search for email
    When I visit the "Home Page"
    And I set the "Email" to "chris@gmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "chris@gmail.com" in the results
    And I should see "Chris" in the results
    And I should not see "john@gmail.com" in the results
    And I should not see "steven@gmail.com" in the results

Scenario: Update a Shopcart
    When I visit the "Home Page"
    And I set the "Name" to "Chris"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Chris" in the "Name" field
    And I should see "chris@gmail.com" in the "Email" field
    When I change "Name" to "Bobby"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Bobby" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Bobby" in the results
    And I should not see "Chris" in the results



Scenario: Delete a Shopcart
    When I visit the "Home Page"
    And I set the "Email" to "chris@gmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    When I press the "Delete" button
    Then I should see the message "Shopcart has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "chris@gmail.com" in the results

Scenario: List items in a shopcart 
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I paste the "Shopcart ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "shirt" in the item results
    And I should see "pants" in the item results

Scenario: Create an item in the shopcart
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I paste the "Shopcart ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    When I set the "Item Name" to "Blouse"
    And I set the "Item Quantity" to "5"
    And I set the "Item Color" to "Pink"
    And I set the "Item Size" to "XL"
    And I set the "Item Price" to "100"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I press the "Clear Item" button
    Then the "Item Name" field should be empty
    And the "Item Quantity" field should be empty
    And the "Item Color" field should be empty
    And the "Item Size" field should be empty
    And the "Item Price" field should be empty
    When I copy the "ID" field
    And I paste the "Shopcart ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "Blouse" in the item results
    And I should see "5" in the item results
    And I should see "Pink" in the item results
    And I should see "XL" in the item results
    And I should see "100" in the item results
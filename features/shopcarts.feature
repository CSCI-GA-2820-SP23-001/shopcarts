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

# Scenario: List all pets
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results

Scenario: Search for name
    When I visit the "Home Page"
    And I set the "Name" to "Chris"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Chris" in the results
    And I should not see "Katelyn" in the results
    And I should not see "Jon" in the results
    And I should not see "Steven" in the results

# Scenario: Search for available
#     When I visit the "Home Page"
#     And I select "True" in the "Available" dropdown
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should see "sammy" in the results
#     And I should not see "leo" in the results

# Scenario: Update a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Loki"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "Loki" in the results
#     And I should not see "fido" in the results

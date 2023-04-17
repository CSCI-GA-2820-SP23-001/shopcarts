Feature: The shopcarts service back-end
    As an E-Commerce Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

Background:
    Given the following shopcarts
        | shopcart_id | name       | email              | phone_number    | date_joined    |
        | 1           | Chris      | chris@gmail.com    | 7575550000      | 02/05/2015     |
        | 2           | Katelyn    | kate@gmail.com     | 5835550987      | 06/21/2000     |
        | 3           | Jon        | john@gmail.com     | 2095558739      | 01/01/2023     |
        | 4           | Steven     | steven@gmail.com   | 2098675535      | 05/14/2005     |


    Given the following items
        | shopcart_id | name       | quantity | color   | size | price |
        | 1           | shirt      | 1        | red     | M    | 20.00 |
        | 1           | pants      | 2        | blue    | S    | 30.00 |
        | 2           | pants      | 1        | black   | L    | 25.00 |
        | 2           | shirt      | 1        | green   | M    | 20.00 |
        | 3           | underwear  | 3        | white   | L    | 15.00 |
        | 4           | headband   | 1        | yellow  | NA   | 5.00  |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart Demo RESTful Service" in the title
    And I should not see "404 Not Found"

# Scenario: Create a Shopcart
#     When I visit the "Home Page"
#     And I set the "Name" to "Happy"
#     And I set the "Category" to "Hippo"
#     And I select "False" in the "Available" dropdown
#     And I select "Male" in the "Gender" dropdown
#     And I set the "Birthday" to "06-16-2022"
#     And I press the "Create" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     Then the "Id" field should be empty
#     And the "Name" field should be empty
#     And the "Category" field should be empty
#     When I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     And I should see "Happy" in the "Name" field
#     And I should see "Hippo" in the "Category" field
#     And I should see "False" in the "Available" dropdown
#     And I should see "Male" in the "Gender" dropdown
#     And I should see "2022-06-16" in the "Birthday" field

# Scenario: List all pets
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Search for dogs
#     When I visit the "Home Page"
#     And I set the "Category" to "dog"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should not see "kitty" in the results
#     And I should not see "leo" in the results

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
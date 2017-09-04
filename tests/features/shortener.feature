Feature: As a user, I want to be able to shorten magnet links into HTTP urls.
        Scenario: I can create a short URL
           Given I have a shortener server up
           When I make a POST request to {base_url}magnet:foobarbazstuff
           Then I receive a body with a string
           When I make a GET request to that string
           Then I get a redirect to magnet:foobarbazstuff
            And I stop the server

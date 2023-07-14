import httpRequest
# from assertions import *

def test_post_three_dishes():
    """
    Test function to insert three dishes using HTTP requests.
    """
    dishes = ["orange", "spaghetti", "apple pie"]
    responses = []

    for dish in dishes:
        response = httpRequest.post("dishes", data={'name': dish})
        responses.append(response)
        assert response.status_code == 201

    assert len(set(response.json() for response in responses)) == len(responses)


def test_get_orange_dish_by_id():
    """
    Test function to get the first dish by id expected to be the orange dish using HTTP requests.
    """
    response = httpRequest.get("/dishes/1")
    assert response.status_code == 200
    dish_data = response.json()
    sodium_amount = dish_data['sodium']
    assert 0.9 <= sodium_amount <= 1.1


def test_get_all_three_dishes():
    """
    Test function to get all dishes. Expected to get three dishes using HTTP requests.
    """
    response = httpRequest.get("dishes")
    assert response.status_code == 200
    dishes_data = response.json()
    assert len(dishes_data) == 3


def test_post_dish_doesnt_exist():
    """
    Test function to insert a dish that doesn't exist using HTTP requests.
    expected to get -3 as a response.
    """
    dish = "blah"
    response = httpRequest.post("dishes", data={'name': dish})

    expected_status_codes = [404, 400, 422]
    assert response.json() == -3
    assert response.status_code in expected_status_codes



def test_post_dish_already_exists():
    """
    Test function to insert a dish that already exists using HTTP requests.
    expected to get -2 as a response.
    """
    dish = "orange"
    response = httpRequest.post("dishes", data={'name': dish})

    expected_status_codes = [404, 400, 422]
    assert response.json() == -2
    assert response.status_code in expected_status_codes



def test_post_meal_with_dishes_id():
    """
    Test function to insert a meal with dish IDs using HTTP requests.
    Expected to get a response with status code 201 and a positive JSON value.
    """
    meal_data = {'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3}
    response = httpRequest.post("meals", data=meal_data)

    assert response.status_code == 201
    assert response.json() > 0


def test_get_all_meals():
    """
    Test function to get all meals. Expected to have one meal in the response with calories between 400 and 500.
    """
    response = httpRequest.get("meals")

    assert response.status_code == 200
    meals_data = response.json()
    assert len(meals_data) == 1
    meal = meals_data["1"]
    assert 400 <= meal['cal'] <= 500


def test_post_meal_already_exists():
    """
    Test function to insert a meal that already exists using HTTP requests.
    expected to get -2 as a response.
    """
    meal_data = {'name': "delicious", 'appetizer': 1, 'main': 2, 'dessert': 3}
    response = httpRequest.post("meals", data=meal_data)

    expected_status_codes = [400, 422]
    assert response.status_code in expected_status_codes
    assert response.json() == -2


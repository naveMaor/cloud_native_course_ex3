import requests
import sys
import httpRequest


def assert_status_code(response: requests.Response, expected_status_code: int) -> None:
    assert response.status_code == expected_status_code


def assert_ret_value(response: requests.Response, expected_value: any) -> None:
    assert response.json() == expected_value


def assert_valid_added_resource(response: requests.Response) -> None:
    assert response.status_code == 201
    # Ensure the returned resource ID is positive
    VALID_RETURNED_RESOURCE_ID = 0
    returned_resource_id = response.json()
    assert returned_resource_id > VALID_RETURNED_RESOURCE_ID


def assert_not_existed_meal(meal_identifier: any) -> None:
    response = httpRequest.get(f"meals/{meal_identifier}")
    assert_status_code(response, expected_status_code=404)
    assert_ret_value(response, expected_value=-5)

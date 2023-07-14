import httpRequest


def main():
    with open('query.txt', 'r') as query_file, open('response.txt', 'w') as response_file:
        for line_number, line in enumerate(query_file, start=1):
            dish_name = line.strip()
            post_response = httpRequest.post("dishes", data={'name': dish_name})
            get_response = httpRequest.get(f"/dishes/{dish_name}")

            if post_response.json() in [-3, -4]:
                response_file.write(
                    f'ERROR.\n')
                continue

            dish_data = get_response.json()
            calories = dish_data['cal']
            sodium = dish_data['sodium']
            sugar = dish_data['sugar']

            # Write to response.txt
            response_file.write(
                f'{dish_name} contains {calories} calories, {sodium} mgs of sodium, and {sugar} grams of sugar\n')
            print(f'{dish_name} contains {calories} calories, {sodium} mgs of sodium, and {sugar} grams of sugar')


if __name__ == "__main__":
    main()

from flask import Flask, jsonify, request

app = Flask(__name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]
dishes = []
meals = []

dishCounter = 0


@app.route('/dishes', methods=['POST'])
def add_dish():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify(0), 415
    if 'name' not in request.json:
        return jsonify(-1), 400
    if request.json['name'] == '':
        return jsonify(-1), 400
    for d in dishes:
        if d['name'] == request.json['name']:
            return jsonify(-2), 400

    api_call = call_api_ninjas(request.json['name'])
    if api_call == -3 or api_call == -4:
        return jsonify(api_call), 400

    dishes.append(api_call)
    return jsonify(dishCounter), 201


@app.route('/meals', methods=['POST'])
def create_meal():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(0), 415

    data = request.json
    if 'name' not in data or 'appetizer' not in data or 'main' not in data or 'dessert' not in data:
        return jsonify(-1), 400

    for meal in meals:
        if meal['name'] == data['name']:
            return jsonify(-2), 400

    for dish_id in [data['appetizer'], data['main'], data['dessert']]:
        if not any(dish['ID'] == dish_id for dish in dishes):
            return jsonify(-5), 404

    meal_id = max([meal['ID'] for meal in meals]) + 1 if meals else 1

    appetizer = next((dish for dish in dishes if dish['ID'] == data['appetizer']), None)
    main = next((dish for dish in dishes if dish['ID'] == data['main']), None)
    dessert = next((dish for dish in dishes if dish['ID'] == data['dessert']), None)

    meal_cal = appetizer['cal'] + main['cal'] + dessert['cal']
    meal_sodium = appetizer['sodium'] + main['sodium'] + dessert['sodium']
    meal_sugar = appetizer['sugar'] + main['sugar'] + dessert['sugar']

    new_meal = {
        'name': data['name'],
        'ID': meal_id,
        'appetizer': data['appetizer'],
        'main': data['main'],
        'dessert': data['dessert'],
        'cal': meal_cal,
        'sodium': meal_sodium,
        'sugar': meal_sugar
    }
    meals.append(new_meal)

    return jsonify(meal_id), 201


@app.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    meal = next((m for m in meals if m['ID'] == meal_id), None)
    if meal is None:
        return jsonify(-1), 400

    if not request.json or 'name' not in request.json or 'appetizer' not in request.json or 'main' not in request.json or 'dessert' not in request.json:
        return jsonify(-1), 400

    meal['name'] = request.json['name']
    meal['appetizer'] = request.json['appetizer']
    meal['main'] = request.json['main']
    meal['dessert'] = request.json['dessert']

    # Compute total calories, sodium, and sugar
    total_calories = 0
    total_sodium = 0
    total_sugar = 0
    for dish_id in (meal['appetizer'], meal['main'], meal['dessert']):
        dish = next((d for d in dishes if d['ID'] == dish_id), None)
        if dish is None:
            return jsonify(-5), 400
        total_calories += dish['cal']
        total_sodium += dish['sodium']
        total_sugar += dish['sugar']
    meal['cal'] = total_calories
    meal['sodium'] = total_sodium
    meal['sugar'] = total_sugar

    return jsonify(meal_id), 200


@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes_indexed = {}
    i = 1
    for dish in dishes:
        dishes_indexed[i] = dish
        print(dish)
        i += 1
    return jsonify(dishes_indexed)


@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish_by_id(dish_id):
    for dish in dishes:
        if dish['ID'] == dish_id:
            return jsonify(dish)
    return jsonify(-5), 404


@app.route('/dishes/<string:dish_name>', methods=['GET'])
def get_dish_by_name(dish_name):
    for dish in dishes:
        if dish['name'] == dish_name:
            return jsonify(dish)
    return jsonify(-5), 404


@app.route('/meals', methods=['GET'])
def get_all_meals():
    all_meals = {}
    i = 1
    for meal in meals:
        all_meals[i] = meal
        i += 1
    return jsonify(all_meals)


# get meal by id
@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal_by_id(meal_id):
    meal = next((m for m in meals if m['ID'] == meal_id), None)
    if meal is None:
        return jsonify(-5), 404
    return jsonify(meal)


@app.route('/meals/<string:meal_name>', methods=['GET'])
def get_meal_by_name(meal_name):
    for meal in meals:
        if meal['name'] == meal_name:
            return jsonify(meal)
    return jsonify(-5), 404


@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal_by_id(meal_id):
    for meal in meals:
        if meal['ID'] == meal_id:
            meals.remove(meal)
            return jsonify(meal_id), 200
    return jsonify(-5), 404


@app.route('/meals/<string:meal_name>', methods=['DELETE'])
def delete_meal_by_name(meal_name):
    for meal in meals:
        if meal['name'] == meal_name:
            meals.remove(meal)
            return jsonify(meal_name), 200
    return jsonify(-5), 404


@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish_by_id(dish_id):
    for dish in dishes:
        if dish['ID'] == dish_id:
            dishes.remove(dish)
            return jsonify(dish_id), 200
    return jsonify(-5), 404


@app.route('/dishes/<string:dish_name>', methods=['DELETE'])
def delete_dish_by_name(dish_name):
    for dish in dishes:
        if dish['name'] == dish_name:
            dishes.remove(dish)
            return jsonify(dish['ID']), 200
    return jsonify(-5), 404


@app.route('/dishes', methods=['DELETE'])
def delete_dishes():
    return jsonify(-1), 400


@app.route('/meals', methods=['DELETE'])
def delete_meals():
    return jsonify(-1), 400


def call_api_ninjas(dish_name):
    import requests
    url = "https://api.api-ninjas.com/v1/nutrition"
    querystring = {"query": dish_name}
    headers = {
        'x-api-key': "QnxHXQzWaSixiioKDlLGSw==JhgDyvuOvc9up9Xj",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code != requests.codes.ok:
        return -4
    if response.text == '[]':
        return -3

    global dishCounter
    dishCounter += 1

    total_calories = 0
    total_serving_size_g = 0
    total_sodium_mg = 0
    total_sugar_g = 0

    for dish in response.json():
        total_calories += dish['calories']
        total_serving_size_g += dish['serving_size_g']
        total_sodium_mg += dish['sodium_mg']
        total_sugar_g += dish['sugar_g']

    dish = {'name': dish_name
        , 'ID': dishCounter
        , 'cal': total_calories
        , 'size': total_serving_size_g
        , 'sodium': total_sodium_mg
        , 'sugar': total_sugar_g
            }
    return dish


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)

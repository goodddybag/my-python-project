from flask import Flask, jsonify, request
from flask_cors import CORS  # Importing the CORS module
import requests  # To make HTTP requests to the Numbers API

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_armstrong(number):
    digits = [int(digit) for digit in str(number)]
    return sum([digit ** len(digits) for digit in digits]) == number

def sum_of_digits(number):
    return sum(int(digit) for digit in str(number))

def get_fun_fact(number):
    # Call Numbers API to get a fun fact about the number
    url = f"http://numbersapi.com/{number}?json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("text", "No fun fact found!")
    else:
        return "No fun fact found!"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    if 'number' not in request.args:
        return jsonify({"error": "Missing 'number' parameter. Please provide a number."}), 400

    try:
        number = int(request.args.get('number'))

        if number < 0:
            return jsonify({"error": "Please enter a positive integer."}), 400

    except ValueError:
        return jsonify({"error": "Invalid input. Please enter a valid integer."}), 400

    # Perform checks
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    odd_or_even = "Even" if number % 2 == 0 else "Odd"
    digit_sum = sum_of_digits(number)

    # Build properties list based on the conditions
    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd_or_even == "Odd":
        properties.append("odd")
    elif odd_or_even == "Even":
        properties.append("even")

    # Fetch fun fact from the Numbers API
    fun_fact = get_fun_fact(number)

    # Build response with explicit Armstrong information
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "is_armstrong": armstrong,
        "properties": properties,  # Now the list will not include empty strings
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=False) 

from flask import Flask, jsonify, request
from flask_cors import CORS  # Importing the CORS module

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

    # Optionally, replace with dynamic fun fact from Numbers API
    fun_fact = f"{number} is an interesting number!"

    # Build response
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": ["armstrong" if armstrong else "", "odd" if odd_or_even == "Odd" else "even"],
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
app.run(host="0.0.0.0", port=10000, debug=False) 

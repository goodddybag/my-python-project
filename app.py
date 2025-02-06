from flask import Flask, jsonify, request
from flask_cors import CORS  # Importing the CORS module
import asyncio
import aiohttp
from flask_caching import Cache

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set up cache for storing fun facts
app.config['CACHE_TYPE'] = 'simple'  # Using simple in-memory cache
cache = Cache(app)

# Asynchronous function to get fun facts from Numbers API
async def get_fun_fact_async(number):
    url = f"http://numbersapi.com/{number}?json"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("text", "No fun fact found!")
        except asyncio.TimeoutError:
            return "Fun fact request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

# Memoization of fun fact to avoid repeated API calls
@cache.memoize(timeout=3600)  # Cache for 1 hour
async def get_fun_fact(number):
    return await get_fun_fact_async(number)

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
async def classify_number():
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

    # Fetch fun fact asynchronously
    fun_fact = await get_fun_fact(number)

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
    import os  # Import os to get the environment variable for port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)

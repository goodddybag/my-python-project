from flask import Flask, jsonify, request
from flask_cors import CORS
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

# Manual caching of fun facts (no async caching support here)
def get_fun_fact_from_cache(number):
    fun_fact = cache.get(f"fun_fact_{number}")
    if fun_fact is None:
        fun_fact = asyncio.run(get_fun_fact_async(number))  # Ensure we wait for the async function
        cache.set(f"fun_fact_{number}", fun_fact, timeout=3600)  # Cache for 1 hour
    return fun_fact

# Sync function to handle number checks
def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    if not number.is_integer():  # Only integers can be perfect numbers
        return False
    number = int(number)  # Convert to integer for perfect number check
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_armstrong(number):
    if not number.is_integer():  # Armstrong numbers only apply to integers
        return False
    digits = [int(digit) for digit in str(int(number))]
    return sum([digit ** len(digits) for digit in digits]) == int(number)

def sum_of_digits(number):
    return sum(int(digit) for digit in str(abs(int(number))))  # Handle absolute value for digits

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    if 'number' not in request.args:
        return jsonify({"error": "Missing 'number' parameter. Please provide a number."}), 400

    # Retrieve the number from the request
    number_str = request.args.get('number')
    try:
        # Try to handle floating-point and integer cases
        number = float(number_str)  # Change this line to support both integers and floats
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter a valid number.", "number": number_str}), 400

    # Perform checks for numbers
    prime = is_prime(number) if number.is_integer() else False
    perfect = is_perfect(number) if number.is_integer() else False
    armstrong = is_armstrong(number) if number.is_integer() else False
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

    # Fetch fun fact synchronously
    fun_fact = get_fun_fact_from_cache(number)

    # Build response
    result = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "is_armstrong": armstrong,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(result)  # Always return 200 OK

# Run the app
if __name__ == '__main__':
    import os  # Import os to get the environment variable for port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)

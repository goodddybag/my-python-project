from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
import aiohttp
from flask_caching import Cache

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set up cache for storing fun facts
app.config['CACHE_TYPE'] = 'simple'
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

# Manual caching of fun facts
def get_fun_fact_from_cache(number):
    # Use the integer part of the number for fun fact
    integer_part = int(number)
    fun_fact = cache.get(f"fun_fact_{integer_part}")
    if fun_fact is None:
        fun_fact = asyncio.run(get_fun_fact_async(integer_part))  # Use integer part for fun fact
        cache.set(f"fun_fact_{integer_part}", fun_fact, timeout=3600)  # Cache for 1 hour
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
    if number < 0:
        return False  # Negative numbers are not perfect
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_armstrong(number):
    if number < 0:
        return False  # Negative numbers can't be Armstrong
    digits = [int(digit) for digit in str(number)]
    return sum([digit ** len(digits) for digit in digits]) == number

def sum_of_digits(number):
    # Convert to a string, remove the decimal point if present, and sum the digits
    return sum(int(digit) for digit in str(abs(number)).replace('.', ''))  # Remove the decimal point

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.getlist('number')
    results = []

    for num_str in number_param:
        result = {
            "number": num_str
        }

        try:
            # Try to convert 'number' to a float to handle both integers and floating-point numbers
            number = float(num_str)
            
            # Convert float to integer for checks if no decimal part is present
            integer_part = int(number) if number.is_integer() else int(number)
            
            # Perform checks
            prime = is_prime(integer_part)
            perfect = is_perfect(integer_part)
            armstrong = is_armstrong(integer_part)
            odd_or_even = "Even" if integer_part % 2 == 0 else "Odd"
            digit_sum = sum_of_digits(number)

            # Build properties list based on the conditions
            properties = []
            if armstrong:
                properties.append("armstrong")
            if odd_or_even == "Odd":
                properties.append("odd")
            elif odd_or_even == "Even":
                properties.append("even")

            # Fetch fun fact synchronously (use the original number for fun fact)
            fun_fact = get_fun_fact_from_cache(number)

            # Add valid results
            result.update({
                "is_prime": prime,
                "is_perfect": perfect,
                "is_armstrong": armstrong,
                "properties": properties,
                "digit_sum": digit_sum,
                "fun_fact": fun_fact
            })
        
        except ValueError:
            # If invalid number, add error message to result
            result["error"] = "Invalid number format."

        results.append(result)

    # Return a 200 OK status with results for all numbers
    return jsonify(results), 200

# Run the app
if __name__ == '__main__':
    import os  # Import os to get the environment variable for port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)

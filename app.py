from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
import aiohttp
from flask_caching import Cache
​
app = Flask(_name_)
​
# Enable CORS for all routes
CORS(app)
​
# Set up cache for storing fun facts
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
​
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
​
# Manual caching of fun facts
def get_fun_fact_from_cache(number):
    integer_part = int(number)  # Use integer part for fun fact
    fun_fact = cache.get(f"fun_fact_{integer_part}")
    if fun_fact is None:
        fun_fact = asyncio.run(get_fun_fact_async(integer_part))
        cache.set(f"fun_fact_{integer_part}", fun_fact, timeout=3600)  # Cache for 1 hour
    return fun_fact
​
# Helper functions
def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True
​
def is_perfect(number):
    if number < 0:
        return False
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number
​
def is_armstrong(number):
    if number < 0:
        return False
    digits = [int(digit) for digit in str(number)]
    return sum([digit ** len(digits) for digit in digits]) == number
​
def sum_of_digits(number):
    return sum(int(digit) for digit in str(abs(number)).replace('.', ''))
​
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.getlist('number')
    results = []
​
    for num_str in number_param:
        try:
            number = float(num_str)
            integer_part = int(number) if number.is_integer() else number
​
            prime = is_prime(integer_part)
            perfect = is_perfect(integer_part)
            armstrong = is_armstrong(integer_part)
            odd_or_even = "even" if integer_part % 2 == 0 else "odd"
            digit_sum = sum_of_digits(integer_part)
​
            properties = []
            if armstrong:
                properties.append("armstrong")
            properties.append(odd_or_even)
​
            fun_fact = get_fun_fact_from_cache(integer_part)
​
            result = {
                "number": integer_part,
                "is_prime": prime,
                "is_perfect": perfect,
                "is_armstrong": armstrong,
                "properties": properties,
                "digit_sum": digit_sum,
                "fun_fact": fun_fact
            }
            results.append(result)
        except ValueError:
            return jsonify({"error": "Invalid number format.", "number": num_str}), 400
​
    return jsonify(results), 200
​
if _name_ == '_main_':
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)

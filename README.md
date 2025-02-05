# Number Classifier API
This API allows you to classify numbers based on various mathematical properties. The API takes a number as input and returns a JSON response with information about whether the number is prime, perfect, Armstrong, odd/even, the sum of its digits, and a fun fact about the number.

# Features
* Prime Check: Determines whether the number is prime.
* Perfect Number Check: Determines whether the number is a perfect number.
* Armstrong Number Check: Determines whether the number is an Armstrong number.
* Odd/Even Check: Determines whether the number is odd or even.
* Sum of Digits: Computes the sum of the digits of the number.
* Fun Fact: Retrieves a fun fact about the number using the Numbers API.

 # Installation 
 1. Clone the repository:
       ```bash
       git clone <repository_url>
       ```
 3. Navigate to the project directory:
       ```bash
       cd my-python-project
       ```
 4. Create and activate a virtual environment:
      ```bash
       python -m venv venv
       source venv/bin/activate  # On Windows use: venv\Scripts\activate
      ```
 5. Install the required dependencies:
    ```bash
       pip install -r requirements.txt
    ```
 
  # Running the API
  Once your project is set up, you can start the API server using Flask:
       ``` bash 
       python app.py
       ```

   # API Usage
   To classify a number, send a GET request to the following URL:
      ```bash
      http://127.0.0.1:5000/api/classify-number?number=300
      ```

   # Example Response:
     For the input 371, the response will be:
     ```bash
     {
          "number": 371,
          "is_prime": false,
          "is_perfect": false,
          "properties": ["armstrong", "odd"],
          "digit_sum": 11,
          "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
    }
    ```
   # Error Handling
   If the provided number is not valid, the API will return a 400 Bad Request with an error message:
           ```bash
              {
                 "number": "abc",
                  "error": true
               }
             ```
   # CORS Support
    The API has CORS enabled, allowing it to be accessed from different domains.

   # License
   This project is open-source and available under the MIT License.
     
   
   
       

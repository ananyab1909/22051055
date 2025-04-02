

from flask import Flask, jsonify, request
import requests
import time
import json

app = Flask(__name__)

URLS = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand"
}

window = 10
numbers = []

def fetch():
    global numbers
    user_numbers_json = request.args.get('numbers') 

    if not user_numbers_json:
        return []  
    try:
        new_numbers = json.loads(user_numbers_json)  
        if not isinstance(new_numbers, list):
            return []  
    except (ValueError, TypeError):
        return []  

    for num in new_numbers:
        if num not in numbers:
            numbers.append(num)
            if len(numbers) > window: 
                numbers.pop(0)

    return new_numbers 

@app.route("/numbers/<string:id>", methods=["GET"])
def get(id):
    if id not in URLS:
        return jsonify({"error": "Invalid number ID."}), 400

    newnum = fetch()  

    avg = round(sum(numbers) / len(numbers), 2) if numbers else 0.0
    response = {
        "windowPrevState": numbers[:-len(newnum)] if len(numbers) >= len(newnum) else [],
        "windowCurrState": numbers,
        "numbers": newnum,
        "avg": avg
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="localhost", port=9876, debug=True)

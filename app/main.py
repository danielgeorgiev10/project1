from flask import Flask, jsonify
import os
import mysql.connector
import time

app = Flask(__name__)

env_name = os.getenv('APP_ENV', 'unknown')
max_n = int(os.getenv('MAX_FIBONACCI', 100))
secret_key = os.getenv('APP_SECRET_KEY', 'no-key')

@app.route("/")
def index():
    return jsonify({
        "message": f"Welcome to Project-App API! Mode: {env_name}",
        "max_allowed": max_n,
        "endpoints": {
            "health": "/health",
            "metadata": "/meta",
            "fibonacci": "/fibonacci/<n>",
            "config": "/config"
        },
        "usage": "Add /fibonacci/<n> to the URL to calculate Fibonacci numbers."
    })

def fibonacci(n):
    if n <= 0: return 0
    elif n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mariadb-service'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        database='fibonacci_db'
    )



def save_to_db(n, result):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO results (n, val) VALUES (%s, %s)", (n, str(result)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to DB: {e}") 

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/fibonacci/<int:n>")
def get_fibonacci(n):
    if n > max_n:
        return jsonify({"error": f"Number is too large. Max is {max_n}."}), 400
    
    result = fibonacci(n)
    save_to_db(n, result)

    return jsonify({
        "input": n,
        "result": result,
        "formula": "F(n) = F(n-1) + F(n-2)"
    })

if __name__ == "__main__":

    port=int(os.getenv('APP_PORT', 5000))
    app.run(host="0.0.0.0", port=port)
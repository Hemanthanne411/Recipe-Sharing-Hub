import os
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import psycopg2
from flask_bcrypt import Bcrypt
import requests
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24) # Persistent session for 24 hours
bcrypt = Bcrypt(app)

# The user-service handles front end too.

# Database connection details
DB_NAME = os.getenv('POSTGRES_DB', 'recipe_app_db')
DB_USER = os.getenv('POSTGRES_USER', 'app_user')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'mysecretpassword6432')
DB_HOST = os.getenv('POSTGRES_HOST', 'postgres-service')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

# Internal API endpoint for the recipe service
RECIPE_API_URL = "http://recipe-service:6002"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

# Navigation Route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# API end points for user-management

# These endpoints directly process the business logic
# 1
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Username already exists."}), 409
    finally:
        cur.close()
        conn.close()
# 2
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.check_password_hash(user[1], password):
        session['username'] = username
        session['user_id'] = user[0]
        session.permanent = True  # Make the session permanent
        return jsonify({"message": "Logged in successfully!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401

# 3
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

# --- Navigation Routes ---

# Navigation Route to render html templates
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('main_dashboard.html')
    return redirect(url_for('index'))

# Navigation Route
@app.route('/add')
def add_recipe_page():
    if 'user_id' in session:
        return render_template('add_recipe.html')
    return redirect(url_for('index'))

# Navigation Route
@app.route('/list')
def list_recipes_page():
    if 'user_id' in session:
        return render_template('list_recipes.html')
    return redirect(url_for('index'))

# --- Proxy Endpoints for the Recipe Service ---
# These routes are to forward requests to the recipe-service and donot process the business logic.
@app.route('/api/add_recipe', methods=['POST'])
def add_recipe_proxy():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    data['user_id'] = session['user_id']
    response = requests.post(f"{RECIPE_API_URL}/add_recipe", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/api/list_recipes', methods=['GET'])
def list_recipes_proxy():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = session['user_id']
    # Using requests library to forward.
    response = requests.get(f"{RECIPE_API_URL}/list_recipes/{int(user_id)}") # User Id is also sent.
    return jsonify(response.json()), response.status_code

@app.route('/api/search_recipe', methods=['GET'])
def search_recipe_proxy():
    query = request.args.get('query')
    response = requests.get(f"{RECIPE_API_URL}/search_recipe", params={'query': query})
    return jsonify(response.json()), response.status_code

# --- New endpoint to fetch recent recipes ---
@app.route('/api/recent_recipes', methods=['GET'])
def recent_recipes_proxy():
    response = requests.get(f"{RECIPE_API_URL}/recent_recipes")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
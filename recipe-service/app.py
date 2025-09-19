import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection details
DB_NAME = os.getenv('POSTGRES_DB', 'recipe_app_db')
DB_USER = os.getenv('POSTGRES_USER', 'app_user')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'mysecretpassword6432')
DB_HOST = os.getenv('POSTGRES_HOST', 'postgres-service')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES (%s, %s, %s, %s)",
            (user_id, title, ingredients, instructions)
        )
        conn.commit()
        return jsonify({"message": "Recipe added successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/list_recipes/<int:user_id>', methods=['GET'])
def list_recipes(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM recipes WHERE user_id = %s", (user_id,))
        recipes = cur.fetchall()
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/search_recipe', methods=['GET'])
def search_recipe():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        search_pattern = f"%{query}%"
        cur.execute(
            "SELECT * FROM recipes WHERE title ILIKE %s OR ingredients ILIKE %s",
            (search_pattern, search_pattern)
        )
        recipes = cur.fetchall()
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# --- New endpoint to fetch the 3 most recent recipes ---
@app.route('/recent_recipes', methods=['GET'])
def recent_recipes():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM recipes ORDER BY created_at DESC LIMIT 3")
        recipes = cur.fetchall()
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002)
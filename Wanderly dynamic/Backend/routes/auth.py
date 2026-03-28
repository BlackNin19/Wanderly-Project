from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, name, email, password, city
        FROM users
        WHERE email = %(email)s
    """, {"email": email})

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"message": "User not found"}), 401

    db_password = user[3]

    if password != db_password:
        cursor.close()
        conn.close()
        return jsonify({"message": "Invalid password"}), 401

    result = {
        "message": "Login successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2],
        "city": user[4]
    }

    cursor.close()
    conn.close()

    return jsonify(result)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    city = data.get("city")

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT user_id FROM users WHERE email = %(email)s",
        {"email": email}
    )

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Email already registered"}), 400

    # Insert new user
    cursor.execute("""
        INSERT INTO users (name, email, password, city)
        VALUES (%(name)s, %(email)s, %(password)s, %(city)s)
    """, {
        "name": name,
        "email": email,
        "password": password,
        "city": city
    })

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Signup successful"})

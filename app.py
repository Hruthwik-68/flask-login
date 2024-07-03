from flask import Flask, request, jsonify, render_template, redirect, url_for
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.id import ID

app = Flask(__name__)

# Initialize the Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Replace with your Appwrite endpoint
client.set_project('667f8c85002229461ca8')  # Project ID
client.set_key('[YOUR_API_KEY]')  # Replace with your API key

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    nickname = data['nickname']
    password = data['password']
    
    # Initialize Appwrite Account service
    account = Account(client)
    databases = Databases(client)

    try:
        # Create user account
        user = account.create(
            user_id=ID.unique(),
            email=email,
            password=password,
            name=username
        )
        
        # Save user data in the database
        databases.create_document(
            database_id='667f8d010031471a488a',
            collection_id='667f8d16003418fd93a2',
            document_id=ID.unique(),
            data={
                'email': email,
                'name': username,
                'nickname': nickname,
                'password': password,
            }
        )
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    databases = Databases(client)

    try:
        # List all documents in the collection
        result = databases.list_documents(
            database_id='667f8d010031471a488a',
            collection_id='667f8d16003418fd93a2'
        )

        # Check if any document matches the email
        user = None
        for document in result['documents']:
            if document['email'] == email:
                user = document
                break

        if user is None:
            return jsonify({"success": False, "message": "Email not found"}), 404
        
        # Check if the password matches
        if user['password'] == password:
            return jsonify({"success": True, "message": "Login successful"}), 200
        else:
            return jsonify({"success": False, "message": "Incorrect password"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

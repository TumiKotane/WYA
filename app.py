# app.py (Backend using Flask)

from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Dummy user data for demonstration
users = {
    'tumi': {'name': 'Tumi', 'password': 'password', 'location': None},
    'sana': {'name': 'Sana', 'password': 'password', 'location': None},
    # Add more users as needed
}

# JWT secret key for token encoding/decoding
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        raise BadRequest("Username and password are required.")

    user = users.get(username)
    if not user or user['password'] != password:
        raise BadRequest("Invalid username or password.")

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/update_location', methods=['POST'])
@jwt_required()
def update_location():
    user_id = get_jwt_identity()
    lat = request.json.get('lat')
    lng = request.json.get('lng')
    if lat is None or lng is None:
        raise BadRequest("Latitude and longitude are required.")
    users[user_id]['location'] = {'lat': lat, 'lng': lng}
    return jsonify({'success': True}) 

@app.route('/get_friends_locations')
@jwt_required()
def get_friends_locations(): 
    user_id = get_jwt_identity()
    friends_locations = {uid: data['location'] for uid, data in users.items() if uid != user_id and data['location']}
    return jsonify(friends_locations) 

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)


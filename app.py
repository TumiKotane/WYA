# app.py (Backend using Flask)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dummy user data for demonstration
users = {
    'tumi': {'name': 'Tumi', 'location': None},
    'sana': {'name': 'Sana', 'location': None},
    # Add more users as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    user_id = request.form['user_id']
    lat = request.form['lat']
    lng = request.form['lng']
    users[user_id]['location'] = {'lat': lat, 'lng': lng}
    return jsonify({'success': True})

@app.route('/get_friends_locations')
def get_friends_locations():
    user_id = request.args.get('user_id')
    friends_locations = {uid: data['location'] for uid, data in users.items() if uid != user_id and data['location']}
    return jsonify(friends_locations)

if __name__ == '__main__':
    app.run(debug=True)


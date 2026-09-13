from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
# The secret key keeps the connection session secure
app.config['SECRET_KEY'] = 'p2p_secret_key_123!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


# 1. Route to serve the main HTML webpage
@app.route('/')
def index():
    return render_template('index.html')

# 2. Handle when a user connects to the website
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print(f"[SERVER] User joined room: {room}")
    # Tell other users in the room that a new peer arrived
    emit('peer_connected', room=room, include_self=False)

# 3. Relay file metadata (name, size) from sender browser to receiver browser
@socketio.on('file_meta')
def on_file_meta(data):
    room = data['room']
    emit('receive_meta', data, room=room, include_self=False)

# 4. Relay raw chunks of file data from sender browser to receiver browser
@socketio.on('file_chunk')
def on_file_chunk(data):
    room = data['room']
    emit('receive_chunk', data, room=room, include_self=False)

if __name__ == '__main__':
    # Runs the web server locally on port 5000
    print("[SERVER] Web server starting on http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User
from db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/home')
@app.route('/')
def home():  # put application's code here
    rooms = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)

    return render_template('home.html', rooms=rooms)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_input = request.form.get('password')

        user = get_user(username)

        if user:
            flash(f"User already exist. Try different username ", "info")
            return render_template('signup.html')
        else:
            save_user(username=username, password=password_input, email=email)
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            flash(f"Successfully logged in", "success")
            return redirect(url_for('home'))
        else:
            flash(f"Invalid credentials. Try again", "danger")

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/create_room", methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            flash(f"Successfully created room {room_name}.", 'success')
            return redirect(url_for('view_room', room_id=room_id))
        else:
            flash("Failed to create room. Please try again later",'danger')

    return render_template('create_room.html')


@app.route('/rooms/<room_id>')
@login_required
def view_room(room_id):  # put application's code here
    room = get_room(room_id)

    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('view_room.html', room=room,
                               room_members=room_members, username=current_user.username, messages=messages)
    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):  # put application's code here
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        room_members_str = ','.join(existing_room_members)
        message = ''
        if request.method == 'POST':

            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)

            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room edited successfully'
            room_members_str = ','.join(new_members)

        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Only admins can edit room. You are not admin", 404


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))

    data['created_at'] = datetime.now().strftime('%d %b, %H:%M')
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms as frooms

from dots import Game
from room import Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)

colors = [
    'gold', 
    'chartreuse', 
    'blue', 
    'aqua', 
    'blueviolet', 
    'chocolate', 
    'cadetblue', 
    'cornflowerblue',
    'darkcyan',
    'darkorchid'
]

rooms = {}
# [ {room_name: RoomObject} ]

print(rooms)

@socketio.on('connect')
def test_connect():
    print("socket connected: " + request.sid)
    print("rooms: ", rooms)
    # print("rooms: ", frooms())

@socketio.on('disconnect')
def disconnect():   
    print("socket disconnected!! " + request.sid)
    # Improvement: Only remove the game from room if the host of that room left.
    rooms.clear()
    # print(frooms())

@socketio.on('message')
def handle_recieve_msg(data):
    print('Recieved msg: ', data)
    send('Message recieved!!!')

# Creates a new room with host player in it.
# Validations: 
#   1. Room already exists or empty room name
#   2. Empty player name
@socketio.on('create-room')
def create_room(data):
    print("Recieved data:", data)
    print("Request: ", request)
    
    room_name = data['room_name']
    player_name = data['player_name']

    # validate room name and player name 
    if ((room_name.strip()=="") or (room_name in rooms)):
        print("rooms: ", rooms)
        print("Invalid room name or room name already exists!")
        return
    if (player_name.strip()==""):
        print("rooms: ", rooms)
        print("Invalid player name!")
        return

    join_room(room_name)

    # Store the room with current player in it.
    new_room = Room(player_name)
    rooms[room_name] = new_room
    # rooms[room_name] = {'players': [player_name], 'game': None}

    print(rooms)


# Adds a new player to the game
# Validations: 
#   1. Room does not exist
#   2. Empty player name or player name already exists.
#   3. Max player limit reached (10)
@socketio.on('join-room')
def create_room(data):
    print("Recieved data:", data)
    print("Request: ", request)
    
    room_name = data['room_name']
    player_name = data['player_name'] 

    # validate room name and player name 
    if ((room_name.strip()=="") or (room_name not in rooms)):
        print("Invalid room or room does not exists!")
        return
    if (player_name.strip()=="" or (player_name in rooms[room_name].players)):
        print("Invalid player name or player name already exists!")
        return
    if len(rooms[room_name].players) == 10: 
        print("Max player limit reached!!")
        return

    join_room(room_name)

    # Add the player in requested room 
    rooms[room_name].add_player(player_name)
    # rooms[room_name]['players'].append(player_name)

    print(rooms)

    # Notify the people in room - new player has joined.
    emit('join-room', rooms[room_name].get_players_list(), to=room_name)


# Plays the turn by connecting given dots and 
#   Notifies which dots are connected
#   Notifies which blocks are created if any.
#   Updates the player turn according to the dots connection.
@socketio.on('play-turn')
def connect_dot(data):
    # print("connecting dots")
    # print("data: ", data)    

    room_name = data['room_name']
    first_dot = data['first_dot']
    second_dot = data['second_dot']
    player_name = data['player_name']

    next_player_turn = True

    game_ins = rooms[room_name].game
    game_ins.numberOfPlayers = len(rooms[room_name].players)
    if game_ins.create_edge(first_dot, second_dot): 
        closed_blocks = game_ins.is_block_closed(first_dot, second_dot)
        if len(closed_blocks)>0:
            next_player_turn = False

            print (rooms[room_name])

            points_to_add = 2 if len(closed_blocks)==2 else 1
            
            rooms[room_name].add_player_points(points_to_add, player_name)

            emit('close-block', {
                'blocks_index_to_close': closed_blocks,
                'color': colors[rooms[room_name].get_player_index(player_name)]
            }, to=room_name)

            # If all the blocks are closed:
            #     find who has the most points
            #     emit "endgame" event, notifing the winner
            #     clear the game.
            if len(game_ins.closed_blocks) == game_ins.total_number_of_blocks():
                # player with most points
                # print("winner: ", rooms[room_name].get_winner())
                emit('end-game', {
                    'winner': rooms[room_name].get_winner(),
                    'players_points': list(rooms[room_name].players.values())
                }, to=room_name)

        emit('play-turn', {
            'player_name': player_name,
            'first_dot': first_dot,
            'second_dot': second_dot,
            'next_player_turn': next_player_turn
        }, to=data['room_name'])


    game_ins.print_game()

@socketio.on('start-game')
def start_game(data): 
    room_name=data['room_name']
    # print("start game data: ", data)
    # Initialize the game instance
    game_ins = Game()
    game_ins.print_game()
    rooms[room_name].game = game_ins

    emit('start-game', to=room_name)




if __name__ == '__main__':
    socketio.run(app, port='5000')


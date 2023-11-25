# Server docs

### Variables

1. `rooms` - List of all the room objects with players in them.

### Endpoints

1. `connect: test_connect()`
	- List current rooms
	- Prints server id of the request connection

2. `disconnect: disconnect()`
	- Prints server id of the server to disconnect
	- Removes all the rooms. <span style="color: grey; opacity: 0.5">***TODO:*** Only remove the room related to the specific connection.</span>

3. `message: handle_recieve_msg(data)`
	- Prints the received data
	- Sends back a received message. <span style="color: grey; opacity: 0.5">***TODO:*** Who does it send the message to?</span>

4. `create-room: create-room(data)`
	- data contains following:
		- `room_name`
		- `player_name`
	- Validates for following:
		- empty `room_name` and `player_name`
		- `room_name` already existing
	- Creates a new room with `room_name` and adds the current player `request.sid` to that room.
	- Also, save the `room_name` and `player_name` in local variable `rooms` <span style="color: grey; opacity: 0.5">***TODO:*** Is it needed to track rooms and players in local variable? Can the front manage the player names and server can just use `request.sid` for each player.</span>

5. `join-room: create_room(data)`
	- data contains following:
		- `room_name`
		- `player_name`
	- Validates for following:
		- `room_name` does not exist
		- Empty `player_name` or `player_name` already exists
		- Max player limit reached (10)
	- Adds the current player `request.sid` to the `room_name` room.
	- Also, adds the current `player_name` to the given `room_name` in local `rooms` variable.
	- Notifies all the players in current `room_name` with list of all the players in the game.

6. `start-game: start_game(data)`
	- data contains following:
		- `room_name`
	- <span style="color: grey; opacity: 0.5">***TODO:*** Validate `room_name` exists</span>
	- Creats a new `Game` instance in given `room_name` in local `rooms` variable.
	- Notifies all the players in current `room_name` with message `"start-game"`

7. `play-turn: connect_dot(data)`
	- data contains following:
		- `room_name`
		- `player_name`
		- `first_dot`
		- `second_dot`
	- Local variables
		- `next_player_turn: boolean`
	- Connects the given `first_dot` and `second_dot`
	- If current player closed any blocks in their turn, then add points and keep the turn, otherwise pass the turn to next player.
	- Notify all the players in `room_name` about this move and `next_player_turn`
	- If the dots can't be connected, then do nothing. <span style="color: grey; opacity: 0.5">***TODO:*** Throw an error and notify the current player about invalid move.</span>
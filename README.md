# Dots game
A competitve game to connect more dots than other players to score more points.

To run the server:
- Run the server using script: `./run_server.sh`
- The app should be now listening on port 5000

To run the client (web app):
- Create a `.env` file and set `SERVER_URL` to the server endpoint. 
    - Example: `SERVER_URL=localhost:5000`  || `SERVER_URL=http://server-endpoint.com`
- Run the client using script: `./run_client.sh`
- The app should be now listening on port 5001
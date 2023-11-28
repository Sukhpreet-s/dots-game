from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)

SERVER_URL = os.environ.get("SERVER_URL", "localhost:5000")
print("SERVER_URL: ", SERVER_URL)

@app.route('/')
def hello_world():
    return render_template("test-client.html", server_url=SERVER_URL)


if __name__ == '__main__':
    app.run(port="5001")
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Enabling cors
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://github-auth-project-ca4p1f8l1-andrewkizito.vercel.app",
            ]
        }
    },
)

# Reading environment variables
client_id = "e664ee93c6721f3a68d4"
client_secret = "6adfaf47e2fe16a6003ea23a1dac98b8fb1e85a6"


@app.route("/auth/callback", methods=["POST"])
def callback():
    # Parsing data
    data = request.json

    # Check if 'code' is in the data dictionary
    if "code" in data:
        code = data.get("code")

        if code:
            try:
                response = requests.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                if response.status_code == 200:
                    data = response.json()
                    if "access_token" in data:
                        return jsonify({"access_token": data["access_token"]}), 200
                    else:
                        return make_response(data["error_description"]), 404
                else:
                    error_message = response.text
                    return make_response(
                        f"Failed to obtain access token: {error_message}", 404
                    )
            except Exception as e:
                error_message = str(e)
                return make_response(f"Failed: {error_message}", 500)
    else:
        return make_response("Code is required", 400)


if __name__ == "__main__":
    app.run(debug=True)

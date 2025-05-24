import secrets

from flask import Flask, jsonify, render_template, request
from nectar import Hive
from nectar.account import Account
from nectargraphenebase.account import PublicKey
from nectargraphenebase.ecdsasig import verify_message

app = Flask(__name__)

# Initialize Hive instance
hive = Hive()

# Simple in-memory token store: {token: username}
sessions = {}


@app.route("/login", methods=["POST"])
def login():
    """
    Accepts a POST request with a Hive Keychain signature and verifies it.
    Expects JSON with: challenge (signature), username, pubkey, proof (message).
    Returns a session token if successful.
    """
    data = request.get_json(force=True)
    required_fields = ["challenge", "username", "pubkey", "proof"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "error": f"Missing field: {field}"}), 400

    signature = data["challenge"]
    username = data["username"]
    pubkey = data["pubkey"]
    message = data["proof"]

    # Fetch posting public keys from blockchain
    try:
        account = Account(username, blockchain_instance=hive)
        posting = account["posting"]
        # Try to handle both dict and list structures
        if isinstance(posting, dict) and "key_auths" in posting:
            # Standard structure
            posting_keys = [
                auth[0] if isinstance(auth, (list, tuple)) else auth["key"]
                for auth in posting["key_auths"]
            ]
        elif isinstance(posting, list):
            # Unexpected: posting is a list
            posting_keys = posting
        else:
            return jsonify({
                "success": False,
                "error": f"Unexpected posting structure: {type(posting)} {posting}",
            }), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Account not found or error: {str(e)}"}), 400

    # Check that provided pubkey is one of the posting keys
    if pubkey not in posting_keys:
        return jsonify({
            "success": False,
            "error": "Provided public key is not a valid posting key for this account.",
        }), 400

    # Verify signature
    try:
        recovered_pubkey_bytes = verify_message(message, bytes.fromhex(signature))
        recovered_pubkey_str = str(PublicKey(recovered_pubkey_bytes.hex(), prefix="STM"))
        valid = recovered_pubkey_str == pubkey
    except Exception as e:
        return jsonify({"success": False, "error": f"Signature verification error: {str(e)}"}), 400

    if not valid:
        return jsonify({"success": False, "error": "Signature is invalid."}), 401

    # Success: generate and return a session token
    token = secrets.token_urlsafe(32)
    sessions[token] = username
    return jsonify({"success": True, "username": username, "token": token})


@app.route("/")
def index():
    """Render the login page."""
    return render_template("login.html")


if __name__ == "__main__":
    # Only run the Flask app if this script is executed directly
    app.run(debug=True, port=8000)

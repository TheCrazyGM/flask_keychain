# Hive Keychain Login Flask Template

This project is a **crude template** for accepting a Hive Keychain login via a Flask web application. It provides a minimal example of how to authenticate users using the Hive Keychain browser extension and a simple Flask backend.

## Features

- Simple login form for Hive usernames
- Integration with the Hive Keychain browser extension
- JavaScript logic separated into `static/js/login.js`
- Flask backend that accepts and verifies login attempts
- Bootstrap-based clean UI

## How It Works

1. **User Login**: The user enters their Hive username and clicks the login button.
2. **Keychain Signing**: The JavaScript requests the user to sign a challenge (current UTC datetime) using their Hive Keychain extension.
3. **Server Verification**: The signed challenge, username, and public key are sent to the Flask backend for verification.
4. **Response**: The server responds with success or error. If successful and a token is returned, it is stored in localStorage.

## Usage Notes

- This is a minimal template and **not production-ready**. It lacks advanced error handling, security hardening, and robust session/token management.
- You must have the Hive Keychain browser extension installed to use the login functionality.
- To run the app, start the Flask server and visit the login page in your browser.

## File Structure

- `templates/login.html`: The login form UI (references external JS)
- `static/js/login.js`: Handles all login and Keychain logic
- `app.py`: Flask backend server

---

Feel free to modify and extend this template to suit your own Hive authentication needs!

from web.main import app  # Import the Flask app from web directory

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
import os
import webbrowser
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# In main:
if __name__ == '__main__':
    print("Opening browser...")
    webbrowser.open('http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
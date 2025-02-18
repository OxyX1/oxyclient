from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def serve_xhtml():
    return send_file("dist/gui/index.xhtml", mimetype="application/xhtml+xml")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    os.system('python dist/ping.py')

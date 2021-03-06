from flask import Flask, render_template_string
from flask_gemoji import Gemoji


app = Flask(__name__)
Gemoji.init_app(app)

@app.route('/')
def index():
    return render_template_string("""
        {{ s | gemoji }}
        {{ s | gemoji(50) }}
        {{ s | gemoji(25) }}
        """, s=":shipit:")

app.run(debug=True)

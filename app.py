import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app) 
app.config['JSON_AS_ASCII'] = False

load_dotenv()
db_url = os.environ.get("DB_URL")
port = os.environ.get("PORT")

@app.before_request
def before_request():
    # check if header inludes authorization
    api_key = request.headers.get("Authorization")
    if api_key == None:
        return Response(status=401)
    
    # check if apikey exists in db
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM wdbcms24_users WHERE api_key = %s", [api_key])
            if cur.fetchone() == None:
                return Response(status=401)

@app.route("/")
def index():
    return { "message": "Hello" }

@app.route("/todos", methods=["GET", "POST"])
def todos():
    return

@app.route("/todos/<id>", methods=["PUT", "DELETE"])
def modify_todo(id):
    return

@app.route("/categories", methods=["GET"])
def categories():
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM wdbcms24_category")
                rows = cur.fetchall()
                print(rows[0])
                return rows

## Kom ihåg:
# - pip install -r requirements.txt
# - Kopiera/byt namn på .env-example ==> .env och sätt in en riktig DB_URL
# - Ändra portnummer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))

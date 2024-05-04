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
    # ignores auth check for cors
    if request.method == "OPTIONS":
        return
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
    api_key = request.headers.get("Authorization")
    if request.method == "GET":
        with psycopg.connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT t.id, t.title, t.done, t.due_date, c.name as category
                            FROM
                                wdbcms24_todo t
                                INNER JOIN wdbcms24_category c ON t.category_id = c.id
                            WHERE
                                t.user_id = (SELECT id FROM wdbcms24_users WHERE api_key = %s)
                            """, [api_key])
                rows = cur.fetchall()
                return rows
    else:
        with psycopg.connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                category = request.json.get("category")
                title = request.json.get("title")
                due_date = request.json.get("due_date")
                # since due_date is optional
                if due_date != None:
                    cur.execute("""
                                INSERT INTO wdbcms24_todo (user_id, category_id, title, due_date) VALUES (
                                    (SELECT id FROM wdbcms24_users WHERE api_key = %s),
                                    (SELECT id FROM wdbcms24_category WHERE name = %s),
                                    %s,
                                    %s
                                )""", [api_key, category, title, due_date])
                else:
                    cur.execute("""
                                INSERT INTO wdbcms24_todo (user_id, category_id, title) VALUES (
                                    (SELECT id FROM wdbcms24_users WHERE api_key = %s),
                                    (SELECT id FROM wdbcms24_category WHERE name = %s),
                                    %s
                                )""", [api_key, category, title])
                return Response(status=200)

@app.route("/todos/<id>", methods=["PUT", "DELETE"])
def modify_todo(id):
    api_key = request.headers.get("Authorization")
    if request.method == "PUT":
        with psycopg.connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                done = request.json.get("done")
                cur.execute("""
                            UPDATE wdbcms24_todo
                            SET done = %s
                            WHERE
                                id = %s AND
                                user_id = (SELECT id FROM wdbcms24_users WHERE api_key = %s)
                            """, [done, id, api_key])
                return Response(status=200)
    else:
        with psycopg.connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            DELETE FROM wdbcms24_todo
                            WHERE
                                id = %s AND
                                user_id = (SELECT id FROM wdbcms24_users WHERE api_key = %s)
                            """, [id, api_key])
                return Response(status=200)

@app.route("/categories", methods=["GET"])
def categories():
        with psycopg.connect(db_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM wdbcms24_category")
                rows = cur.fetchall()
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

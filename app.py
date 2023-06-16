from flask import Flask, request, jsonify, make_response
import dbcreds, dbhelpers

app = Flask(__name__)

@app.get("/api/candy")
def get_candy():
    results = dbhelpers.run_procedures("CALL get_candy()", [])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
    
@app.post("/api/candy")
def post_candy():
    error = dbhelpers.check_endpoint_info(request.json, ["name", "image_url", "description"])
    if(error != None):
        return make_response(jsonify(error), 500)
    results = dbhelpers.run_procedures("CALL post_candy(?,?,?)", [request.json.get('name'), request.json.get('image_url'), request.json.get('description')])
    if(type(results) == list):
        return make_response(jsonify(error), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))

@app.delete("/api/candy")
def delete_candy():
    try:
        user_id_input = int(request.args.get("user_id"))
        results = dbhelpers.run_procedures("CALL delete_candy(?)", [user_id_input])

        if isinstance(results, list):
            return make_response(jsonify("Candy deleted successfully"), 200)
        else:
            return make_response(jsonify("Sorry, something went wrong"), 500)
    except Exception as e:
        return make_response(jsonify("Error: " + str(e)), 500)

if(dbcreds.production_mode == True):
    print("Runing in production mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in developer mode")
    app.run(debug=True)
from flask import request, jsonify
from config import app, db
from models import Users

@app.route("/users", methods=["GET"])
def get_users():
    users = Users.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    return jsonify({"users":json_users})

@app.route("/create_user", methods=["POST"])
def create_user():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message":"Fyll i alla fält"}),
            400,
        )

    new_user = Users(first_name=first_name,last_name=last_name, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message":str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

@app.route("/update_contact/<int:user_id>")
def update_user(user_id):
    user = Users.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    user.first_name = data.get("firstName", user.first_name)
    user.last_name = data.get("lastName", user.last_name)
    user.email = data.get("email", user.email)

    db.session.commit()

    return jsonify({"message": "User updated."})

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    user = Users.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    

if __name__== "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
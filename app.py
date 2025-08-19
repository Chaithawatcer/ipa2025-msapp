import os

from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId

#mongo_uri  = os.environ.get("MONGO_URI")
#db_name    = os.environ.get("DB_NAME")

client = MongoClient("mongo:27017")
db = client["mydatabase"]
routers = db["routers"]

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", routers=list(routers.find()))

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect("/")

@app.route("/delete/<id>", methods=["POST"])
def delete_router(id):
    routers.delete_one({"_id": ObjectId(id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
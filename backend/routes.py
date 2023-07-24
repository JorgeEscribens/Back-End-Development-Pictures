from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not id:
        return {"messsage": "No id provided"}, 422
    
    for picture in data:
        if picture["id"] == id:
            return picture
    
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()

    if not picture_data:
        return {"messsage": "No data provided"}, 422

    for picture in data:
        if picture["id"] == picture_data["id"]:
            return {"Message": f"picture with id {picture_data['id']} already present"}, 302

    try:
        data.append(picture_data)
    except NameError:
        return {"messsage": "Wrong data provided"}, 500
    
    return {"id": picture_data["id"], "pic_url": picture_data["pic_url"]}, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.get_json()

    if not picture_data:
        return {"messsage": "No data provided"}, 422

    for picture in data:
        if picture["id"] == picture_data["id"]:
            data.remove(picture)
            data.append(picture_data)
            return {"Message": "Picture updated"}, 200

    return {"messsage": "Picure not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"Message": "Picture deleted"}, 204

    return {"messsage": "Picure not found"}, 404

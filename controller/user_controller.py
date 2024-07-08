from app import app
from model.user_model import user_model
from flask import request

obj = user_model()
@app.route('/user/addone',methods=['POST'])
def user_signup_controller():
    return obj.user_addone_model()

@app.route('/user/allusers',methods=['GET'])
def all_users_controller():
    return obj.getting_all_users()

@app.route('/user/update/<int:id>',methods=['put'])
def user_update_controller(id):
    return obj.user_update_model(id)

@app.route('/user/update/<int:id>',methods=['patch'])
def user_patch_update_controller(id):
    return obj.user_patch_update(id)


@app.route('/user/delete/<int:id>',methods=['delete'])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route('/user/allusers/<int:start>/to/<int:end>',methods=['GET'])
def user_pagginate_controller(start,end):
    return obj.user_pagginate_model(start,end)

@app.route('/user/login',methods=['POST'])
def user_login_controller():
    return obj.user_login_model()
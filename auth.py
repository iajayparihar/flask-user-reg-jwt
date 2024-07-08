from flask import Blueprint, jsonify, request, redirect, url_for
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jti
auth_bp = Blueprint('auth', __name__)
from flask_jwt_extended import get_jwt_identity, jwt_required


from flask_login import logout_user, login_required

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
     
    return jsonify(logged_in_as=current_user), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
@jwt_required()
def logout():
    logout_user()
    return jsonify({"msg":"User logged out succesfully."})
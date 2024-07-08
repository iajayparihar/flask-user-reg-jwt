from app import app
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import datetime

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# login_manager.login_view = 'user_login_controller'
jwt = JWTManager(app)

# Blacklist model
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# Define a model    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f'<User {self.name}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Check if a token has been blacklisted
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).scalar()
    return token is not None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     import pdb;pdb.set_trace()
#     jti = get_jwt()['jti']
#     db.session.add(TokenBlocklist(jti=jti, created_at=datetime.utcnow()))
#     db.session.commit()
#     return jsonify(msg="Successfully logged out"), 200



class user_model():
    def user_addone_model(self):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if name and email and password:
            newUser = User(name=name, email=email, password=hashed_password)
            db.session.add(newUser)
            db.session.commit()
            return jsonify({'msg':'User created successfully'}), 201
        else:
            return jsonify({'msg':'Please fill all the fields'}),400
    
    @login_required
    @jwt_required()
    def getting_all_users(self):
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['name'] = user.name
            user_data['email'] = user.email
            user_data['password'] =  user.password
            output.append(user_data)
        return jsonify({'users': output}),200
    
    @login_required
    @jwt_required()
    def user_update_model(self,id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name and email and password:
            user.name = name
            user.email = email
            user.password =  password
            db.session.commit()
            return f'user {id=} is updated'
        else:
            return jsonify({'msg':'Please fill all the fields'}),400
        
    @login_required
    @jwt_required()
    def user_patch_update(self,id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.form

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']

        db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    
    @login_required
    @jwt_required()
    def user_delete_model(self,id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return f'user {id=} is deleted'
    
    @login_required
    @jwt_required()
    def user_pagginate_model(self,start,end):
        if start < 0 or end <= start:
            return jsonify({"error": "Invalid parameters"}), 400

        users = User.query.order_by(User.id).slice(start, end).all()
        
        user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]

        return jsonify({'payload': user_list})


    def user_login_model(self):
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        login_user(user)
        access_token = create_access_token(identity={'id': user.id, 'name': user.name, 'email': user.email})
        return jsonify(access_token=access_token)
    





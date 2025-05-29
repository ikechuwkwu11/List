from flask import Flask,jsonify,request
from models import User,List,db
from flask_login import LoginManager,login_user,logout_user
from datetime import datetime

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config['SECRET_KEY'] = 'Iyke'
db.init_app(app)

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/list')
def all_list():
    list_all = List.query.all()
    return jsonify({'list':list_all}),200

@app.route('/api/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message':'fill in all forms'}),404

        new_user = User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'You have successfully registered. Now pls login'}),201
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message':'Put in the correct details'}),404

        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            login_user(user)
            db.session.commit()
            return jsonify({'message':'successfully logged in'}),200
        return jsonify({'message':'invalid details, please login again'}),404
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500

@app.route('/api/logout',methods=['GET'])
def logout():
    try:
        logout_user()
        return jsonify({'message':'You have been logged'}),200
    except Exception as e:
        return jsonify({'message':'internal server error','error':str(e)}),500


@app.route('/api/add_list',methods=['POST'])
def add_list():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        started_at = data.get('started_at')
        if not title or not description or not started_at:
            return jsonify({'message':'Please fill in all forms'}),404

        started_at = datetime.fromisoformat(started_at) if started_at else datetime.utcnow()

        new_user = List(title=title,description=description,started_at=started_at)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'You list has been added to your to do list'}),201
    except Exception as e:
        return jsonify({'message':'Internal sever error','error':str(e)}),500

@app.route('/api/all_list',methods=['GET'])
def get_all_lists():
    try:
        list = List.query.all()
        list_all = [
            {
                "title": l.title,
                "description":l.description,
                "started_at":l.started_at
            }
            for l in list
        ]
        return jsonify({'lists':list_all}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/api/single_list/<int:list_id>',methods=['GET'])
def single_list(list_id):
    try:
        list = List.query.get(list_id)
        if not list:
            return jsonify({'message': 'List not found'}), 404

        list_data = {
            'id': list.id,
            'user_id': list.user_id,
            'title': list.title,
            'description': list.description,
            'started_at': list.started_at.isoformat() if list.started_at else None,
            'created_at': list.created_at.isoformat() if list.created_at else None
        }
        return jsonify({'single_list':list_data}),200
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500

@app.route('/api/edit_list/<int:list_id>',methods=['PUT'])
def edit_list(list_id):
    try:
        list = List.query.get(list_id)
        data = request.get_json()
        title = data.get('title', list.title)
        description = data.get('description',list.description)
        started_at = data.get('started_at',list.started_at)
        if not title or not description or not started_at:
            return jsonify({'message':'Please fill in all form'}),404
        db.session.commit()
        return jsonify({'message':'Your list has been updated','data':list.to_dict()}),201
    except Exception as e:
        return jsonify({'message':'Internal server error','error':str(e)}),500



if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

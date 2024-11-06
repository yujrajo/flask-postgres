from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Converter(db.Model):
    __tablename__ = 'converter'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(100), nullable=False)
    checksum = db.Column(db.String(100), nullable=False)

    def json(self):
        return {'id': self.id,'file_name': self.file_name, 'file_path': self.file_path, 'checksum':self.checksum}

with app.app_context():
    db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# add a file to db
@app.route('/converter', methods=['POST'])
def create_file():
  try:
    data = request.get_json()
    file = Converter(file_name=data['file_name'], file_path=data['file_path'], checksum=data['checksum'])
    db.session.add(file)
    db.session.commit()
    return make_response(jsonify({'message': 'file created'}), 201)
  except e:
    return make_response(jsonify({'message': 'error creating file'}), 500)

# get all files
@app.route('/converter', methods=['GET'])
def get_file():
  try:
    files = Converter.query.all()
    return make_response(jsonify([file.json() for file in files]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting file'}), 500)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

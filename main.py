from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)

#* models
class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)
  
  # def __init__(self, name, views, likes):
  #   self.name = name
  #   self.views = views
  #   self.likes = likes
  
  def __repr__(self):
    return f"Video(name={self.name}, views={self.views}, likes={self.likes})"
  
# db.create_all() #* create a database

names = {
  "tim": {
    "age": 19,
    "gender": "male"
  },
  "bill": {
    "age": 70,
    "gender": "male"
  }
}

class HelloWorld(Resource):
  def get(self, name):
    return names[name]
  
  # def post(self):
  #   return {"data": "Posted"}
  
# videos = {}
  
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'likes': fields.Integer
}

# def abort_video(video_id):
#   if video_id not in videos:
#     abort(404, message="Could not find video...")
    
# def abort_video_if_exists(video_id):
#   if video_id in videos:
#     abort(409, message="Video already exists with that ID...")

class Video(Resource):
  @marshal_with(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Could not find video with that id")
    return result
  
  @marshal_with(resource_fields)
  def put(self, video_id):
    # abort_video_if_exists(video_id)
    
    args = video_put_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    
    if result:
      abort(409, message="Video id taken...")
    
    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    print(request.form['likes'])
    
    # videos[video_id] = args
    # return {video_id: args}
    return video, 201  # 201 - created, 200 - okay
  
  def delete(self, video_id):
    abort_video(video_id)
    del videos[video_id]
    return '', 204
  

api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
  app.run(debug=True)
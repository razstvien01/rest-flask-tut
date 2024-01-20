from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)

api = Api(app)

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
  
videos = {}
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

def abort_video(video_id):
  if video_id not in videos:
    abort(404, message="Could not find video...")
    
def abort_video_if_exists(video_id):
  if video_id in videos:
    abort(409, message="Video already exists with that ID...")

class Video(Resource):
  def get(self, video_id):
    abort_video(video_id)
    return videos[video_id]
  
  def put(self, video_id):
    abort_video_if_exists(video_id)
    args = video_put_args.parse_args()
    print(request.form['likes'])
    
    videos[video_id] = args
    # return {video_id: args}
    return videos[video_id], 201  # 201 - created, 200 - okay
  
  def delete(self, video_id):
    abort_video(video_id)
    del videos[video_id]
    return '', 204
  

api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
  app.run(debug=True)
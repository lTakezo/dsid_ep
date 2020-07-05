from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# {"username":"mario", "dest":"São paulo", "type":"Hotel", "name":"Hotel 10/10"}

class Pacotes(Resource):
	def get(self):
		return {'about':'Hello World!'}
		
	def post(self):
		sent = request.form.
		return {'you sent': sent}
		
#class Multi(Resource):
#	def get(self, num):
#		return {'result': num*10}
		
api.add_resource(Pacotes, '/pacotesapi')
#api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
	app.run(debug=True)
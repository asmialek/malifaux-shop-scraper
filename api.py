from flask import Flask
from flask_restful import Resource, Api
import mali_shop_scraper

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        item_list = ['KAERIS CORE BOX','Servants of the Void', 'Beyond Time',]
        return mali_shop_scraper.main(item_list)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask_restful import Resource, Api
import mali_shop_scraper

app = Flask(__name__)
api = Api(app)

class GetMalifauxGoodies(Resource):
    def get(self, item_name):
        item_list = [item_name]
        return mali_shop_scraper.main(item_list)

api.add_resource(GetMalifauxGoodies, '/<string:item_name>')

if __name__ == '__main__':
    app.run(debug=True)
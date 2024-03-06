from flask import Flask, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    try:
        bakeries = Bakery.query.all()
        serialized_bakeries = [bakery.to_dict() for bakery in bakeries]
        return jsonify(serialized_bakeries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    try:
        bakery = Bakery.query.get(id)
        if bakery:
            serialized_bakery = bakery.to_dict()
            return jsonify(serialized_bakery)
        else:
            return jsonify({'error': 'Bakery not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        serialized_baked_goods = [baked_good.to_dict() for baked_good in baked_goods]
        return jsonify(serialized_baked_goods)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    try:
        most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if most_expensive_baked_good:
            serialized_most_expensive = most_expensive_baked_good.to_dict()
            return jsonify(serialized_most_expensive)
        else:
            return jsonify({'error': 'No baked goods found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)

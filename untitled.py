from flask import Flask, request, jsonify
from converter import Converter
from storage import StorageAlchemy

app = Flask(__name__)
c = Converter(StorageAlchemy())

@app.route('/currency_converter', methods=["GET"])
def API():
    args = dict()
    if request.method == 'GET':
        args['input'] = request.args.get("input_currency", type=str)
        args['output'] = request.args.get("output_currency", type=str)
        args['amount'] = request.args.get("amount", type=float)

        if args['amount'] is None:
            return jsonify({"error": "amount not entered"})

        result = c.convert(args['input'], args['output'], args['amount'])

        return jsonify(result)
    else:
        response = jsonify({"error": "wrong http method"})
        response.status_code = 405
        return response

@app.route('/update', methods=['GET'])
def update():
    if request.method == 'GET':
        result = c.db.update_db()
        return jsonify(result)
    else:
        response = jsonify({"error":"wrong http method"})
        response.status_code = 405
        return response

if __name__ == '__main__':
    app.run(debug = True)

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    if not query or len(query) < 10:
        return jsonify({"error": "Invalid query"}), 400
    
    print(query)
    
    return query
    
    
    
if __name__ == '__main__':
    app.run(debug=True)

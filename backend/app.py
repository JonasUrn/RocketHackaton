from flask import Flask, jsonify, request
from flask_cors import CORS

from test import get_user_input
from llama import rephrase_query, rephrase_answer

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
    
    new_query = rephrase_query(query)
    new_query = new_query[1:len(new_query)-1]
    
    print(f"Query: {new_query}")
    
    answer = get_user_input(new_query)
    
    return answer
    
    
if __name__ == '__main__':
    app.run(debug=True)
    

# What is SPbD at IBM?

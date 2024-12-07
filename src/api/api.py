import time
from flask import Flask, request, jsonify
from sql_generator import generate_sql_query
from database_connector import execute_sql_query
from db_conn_config import schema, persona
import pandas as pd

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    start_time = time.time()
    data = request.json
    question = data.get("question")

    # Generate SQL query
    sql_query = generate_sql_query(question, schema, persona)

    # Execute the SQL query
    result = execute_sql_query(sql_query)
    result = result.to_dict(orient="records") 


    response_time = (time.time() - start_time) 
    return jsonify({
                    "natural_language_query": question,
                    "sql_query": sql_query,
                    "result": result,
                    "response_time":f"{response_time:.3f} seconds"
                    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

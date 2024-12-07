
def generate_prompt(question: str) -> str:

    with open("src/api/prompt/persona.txt", "r") as f:
        persona = f.read()

    with open("src/api/prompt/context.txt", "r") as f:
        context = f.read()

    with open("src/api/prompt/schema.sql", "r") as f:
        schema = f.read()

    
    prompt = f""" 

### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Database Schema
The query will run on a database with the following schema:
{schema}

### Answer
Given the database schema, here is the SQL query that [QUESTION]{question}[/QUESTION]
[SQL]
"""
    return prompt



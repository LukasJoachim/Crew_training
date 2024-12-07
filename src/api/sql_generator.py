import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from prompt import generate_prompt
import random
import numpy as np


SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

model_path = "defog/sqlcoder-7b-2"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
        model_path,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        use_cache=True,
    )
model = model.to("cpu") 

def extract_answer(output: str) -> str:
    """
    Extract the SQL query answer from the model's output.
    """
    try:
        # Locate the start of the SQL query in the output
        start_key = "Here is the SQL query that answers the question:"
        answer_start = output.find(start_key)
        if answer_start == -1:
            raise ValueError("Answer not found in the model output.")
        
        # Extract the query and clean up the text
        return output[answer_start + len(start_key):].strip()
    except Exception as e:
        return f"Error extracting answer: {e}"

def generate_sql_query(question: str) -> str:
    """
    Generate an SQL query for the given question using the language model.
    """
    # Generate a properly formatted prompt using your custom function
    prompt = generate_prompt.generate_prompt(question)

    eos_token_id = tokenizer.eos_token_id
    pipe = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=300,
                    do_sample=False,
                    return_full_text=False, # added return_full_text parameter to prevent splitting issues with prompt
                    num_beams=5, # do beam search with 5 beams for high quality results
                    )
    generated_query = (
        pipe(
            prompt,
            num_return_sequences=1,
            eos_token_id=eos_token_id,
            pad_token_id=eos_token_id,
        )[0]["generated_text"]
        .split(";")[0]
        .split("```")[0]
        .strip()
        + ";"
    )

    return generated_query

# Example usage
if __name__ == "__main__":
    question = "Where are all our employees locations?"
    sql_query = generate_sql_query(question)
    print("Generated SQL Query:")
    print(sql_query)
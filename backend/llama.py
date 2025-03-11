import ollama
import re

def rephrase_query(user_query):
    prompt = f"""Rewrite the following user query into a **concise and structured statement** for searching in a database. 
    - **Do not** phrase it as a question.
    - **Use keywords or phrases** instead of full sentences.
    - **Keep it short and to the point**.
    
    Example:
    - "Whatis XC10?" → "XC10 overview"
    - "how use ChromaDB?" → "ChromaDB usage guide"
    - "Tell about AI?" → "Artificial Intelligence introduction"
    
    Now rewrite this query: "{user_query}"
    Fixed Query:
    """
    
    response = ollama.generate(model="llama3.2", prompt=prompt)
    
    return response["response"].strip()

def rephrase_answer(answer, query):
    prompt = f"""
        Summarize the given answer while ensuring clarity and relevance to the query. The answer comes from three different files—select the most relevant parts.

        ### **Guidelines:**
        - **Exclude references to figures, tables, or images.**  
        - **List only the files used at the bottom under 'References'.**  
        - If only 2 of the 3 files were used, reference only those 2.  
        - Only give answer, do not use things like 'Here is a summary of the mainframe information in the given answer:' or similar
        - Strictly follow the below mentioned format

        ### **Input Data:**  
        **Query:** "{query}"  
        **Answer:** "{answer}"  

        ### **Structured Response Format:**
        ALWAYS USE THIS EXACT FORMAT:
        **1. Short Answer:**
        (A brief, 1-2 sentence summary of the most important information)

        **2. Detailed Answer:**
        (A well-structured, in-depth explanation, using only relevant content from the provided answer)

        **3. References:**
        (Only list the file names that contributed to the final answer)
        """
    
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"].strip()
    
    print(content) 
    
    short_answer = ""
    detailed_answer = ""
    references = ""
    
    if "**1. Short Answer:**" in content or "**Short Answer:**" in content:
        short_answer = content.split("**1. Short Answer:**")[1].split("**2. Detailed Answer:**")[0].strip()

    if "**2. Detailed Answer:**" in content or "**Detailed Answer:**" in content:
        detailed_answer = content.split("**2. Detailed Answer:**")[1].split("**3. References:**")[0].strip()

    if "**3. References:**" in content or "**3. References:**" in content:
        references = content.split("**3. References:**")[1].strip()

    return {
        "short_answer": short_answer,
        "detailed_answer": detailed_answer,
        "references": references
    }



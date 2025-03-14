import ollama
import re

def select_best_query(q1, q2, q3, query):
    prompt = f"""You are given a user query and three fixed queries. Your task is to select the best-matching fixed query for the given user query. 
    
    ### Instructions:
    - Analyze which of the three fixed queries aligns most closely with the intent and meaning of the user query.
    - Return **only** the number corresponding to the best query: **1, 2, or 3**.
    - Do **not** provide explanations, reasoning, or any extra text—just the number.

    ### Input:
    User Query: "{query}"  
    Query 1: "{q1}"  
    Query 2: "{q2}"  
    Query 3: "{q3}"  

    ### Output:
    (Return only one number of: 1, 2, or 3)
    """

    response = ollama.generate(model="llama3.2", prompt=prompt)
    response = response["response"].strip()
    
    if response == "1":
        return q1
    elif response == "2":
        return q2
    else:
        return q3
    
def select_best_answer(a1, a2, a3, query, context):
    prompt = f"""You are given a user query, a contextual reference, and three possible answers. Your task is to determine which answer best matches the user query while considering the provided context.

    ### Instructions:
    - Analyze all three answers in relation to the **user query** and **context**.
    - Select the answer that is **most relevant, accurate, and aligned** with the query.
    - Return **only** the number corresponding to the best answer: **1, 2, or 3**.
    - Do **not** provide explanations, reasoning, or any extra text—just the number.

    ### Input:
    **User Query:** "{query}"  
    **Context:** "{context}"  

    **Answer 1:** "{a1}"  
    **Answer 2:** "{a2}"  
    **Answer 3:** "{a3}"  

    ### Output:
    (Return only one number of: 1, 2, or 3)
    """

    response = ollama.generate(model="llama3.2", prompt=prompt)
    response = response["response"].strip()

    if response == "1":
            return a1
    elif response == "2":
            return a2
    else:
            return a3
    

def rephrase_query(user_query):
    prompt = f"""Rewrite the following user query into a **concise and structured keyword phrase** for searching in ChromaDB.

            ### **Rules:**
            - **Return ONLY the fixed query** (no explanations, no extra text).
            - **Do NOT** phrase it as a question.
            - **Use ONLY precise, relevant technical terms.**
            - **DO NOT include unrelated synonyms or broader topics.**
            - **If the query refers to a known technology, keep it exact.**
            - **If unclear, assume it's referring to a standard concept in tech.**
            - **Format the response as: "term1, term2, term3" (maximum 3 terms).**

            ### **Examples:**
            - "What is XC10?" → "XC10 overview, XC10 system architecture"
            - "how use ChromaDB?" → "ChromaDB usage guide, ChromaDB vector search"
            - "Tell about AI?" → "Artificial Intelligence introduction, AI concepts"
            - "Explain me CHROMADB?" → "ChromaDB documentation, ChromaDB architecture"
            - "Tell me information regarding REST Gateway" → "REST Gateway, REST API Gateway, API Gateway documentation"

            ### **Now rewrite the following:**
            User Query: "{user_query}"
            Fixed Query:
            """

    response = ollama.generate(model="llama3.2", prompt=prompt)

    return response["response"].strip()

def rephrase_answer(answer, query, counter):
    prompt = f"""
        Summarize the given answer while ensuring clarity and relevance to the query. The answer comes from three different files—select the most relevant parts.
        The answer must match the context of what user asked in the query.

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
    
    print("=========================================")
    print("CONTENT")
    print("=========================================")
    print(content) 
    print("=========================================")
    print("query")
    print("=========================================")
    print(query)
    print("=========================================")
    
    short_answer = ""
    detailed_answer = ""
    references = ""
    
    if "Short Answer:" not in content or "Detailed Answer:" not in content or "References:" not in content:
        if counter < 3:
                rephrase_answer(answer, query, counter + 1)
        else:
            return {
                "short_answer": "error",
                "detailed_answer": "error",
                "references": "error",
            }
        
    if "**1. Short Answer:**" in content or "**Short Answer:**" in content:
        short_answer = content.split("**1. Short Answer:**")[1].split("**2. Detailed Answer:**")[0].strip()

    if "**2. Detailed Answer:**" in content or "**Detailed Answer:**" in content:
        detailed_answer = content.split("**2. Detailed Answer:**")[1].split("**3. References:**")[0].strip()

    if "**3. References:**" in content or "**3. References:**" in content:
        references = content.split("**3. References:**")[1].strip()
    
    separators = r"[,\n\*\-\+=]"
    references = references.strip()
    ref_list = [ref.strip() for ref in re.split(separators, references) if ref.strip()]

    ref_links = [ref.strip() for ref in ref_list if ref.strip() and "sg" in ref or "redp" in ref]

    return {
        "short_answer": short_answer,
        "detailed_answer": detailed_answer,
        "references": references,
        "links": ref_links
    }



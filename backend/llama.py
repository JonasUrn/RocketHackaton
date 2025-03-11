import ollama
import re

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
    print(query)
    
    short_answer = ""
    detailed_answer = ""
    references = ""
    
    if "**1. Short Answer:**" not in content or "**2. Detailed Answer:**" not in content or "**3. References:**" not in content:
        if "**Short Answer:**" not in content or "**Detailed Answer:**" not in content or "**3. References:**" not in content:
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
    
    ref_list = []
    
    if "," in references:        
        ref_list = references.split(",")
    elif "*" in references:
        ref_list = references.split("*")
    
    ref_links = []
    
    for link in ref_list:
        link_x = link.strip()
        ref_links.append(link_x)

    return {
        "short_answer": short_answer,
        "detailed_answer": detailed_answer,
        "references": references,
        "links": ref_links
    }



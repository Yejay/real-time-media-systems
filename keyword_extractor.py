from keybert import KeyBERT
import os

def extract_keywords(text: str, output_name: str, num_keywords: int = 10) -> str:
    """Extract keywords from transcribed text using KeyBERT"""
    
    # Initialize KeyBERT model
    kw_model = KeyBERT()
    
    # Extract keywords
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), 
                                       stop_words='german', top_k=num_keywords)
    
    # Format keywords
    keyword_content = "# Extracted Keywords\n\n"
    for keyword, score in keywords:
        keyword_content += f"- {keyword} (Score: {score:.3f})\n"
    
    # Save keywords file
    keywords_path = f"output/{output_name}_keywords.txt"
    os.makedirs("output", exist_ok=True)
    
    with open(keywords_path, "w", encoding="utf-8") as f:
        f.write(keyword_content)
    
    return keywords_path

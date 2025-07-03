from transformers import AutoModelForTokenClassification, AutoTokenizer
import requests
from bs4 import BeautifulSoup
import torch

model_path = "product_model_ner"

# Load model and tokenizer
model = AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def check_is_url_parsing(url):
  headers = {"User-Agent": "Mozilla/5.0"}
  try:
      response = requests.get(url, headers=headers, timeout=10)
      response.raise_for_status() #check for html error
      soup = BeautifulSoup(response.text, "html.parser")

      return True

  except requests.exceptions.RequestException as e:
    print(f"Attemp to URL falied: {e}")
    return False
  

def extract_top_product_names(url, max_length=80, min_length=0, top_n=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    blacklist_tags = {"footer", "nav", "script", "style", "noscript", "form", "aside", "ul", "li"}
    candidates = {}

    def add_candidate(text, source):
        text = text.strip()
        if "$" in text:
          return
        if min_length < len(text) <= max_length:
            candidates[text] = source

    # 1. h1
    h1 = soup.find("h1")
    if h1:
        add_candidate(h1.get_text(), "h1")

    # 2. h2 и h3
    for tag in soup.find_all(["h2", "h3"]):
        if tag.find_parent(blacklist_tags): continue
        add_candidate(tag.get_text(), tag.name)

    # 3. By keywords in class
    class_keywords = ["product__", "product-","title"]
    for tag in soup.find_all(True):
        classes = tag.get("class")
        if not classes:
            continue
        if any(any(k in cls.lower() for k in class_keywords) for cls in classes):
            if tag.find_parent(blacklist_tags): continue
            add_candidate(tag.get_text(), f"class={','.join(classes)}")

    # Longer textes can provide better information
    sorted_candidates = sorted(candidates.items(), key=lambda x: len(x[0]), reverse=True)

    return sorted_candidates[:top_n]


def predict(url):
    try:
        if(check_is_url_parsing(url)):
            raw_text = extract_top_product_names(url)

            texts = [t[0] for t in raw_text]
            encoded = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, is_split_into_words=True)

            with torch.no_grad():
                outputs = model(**encoded)
            
            predictions = torch.argmax(outputs.logits, dim=2)

            results = []
            for i, text in enumerate(texts):
                token_ids = encoded["input_ids"][i]
                tokens = tokenizer.convert_ids_to_tokens(token_ids)
                labels = [model.config.id2label[p.item()] for p in predictions[i]]
                results.append(list(zip(tokens, labels)))

            return results
        
    except Exception as e:
        print(f"Error occuring: {e}")

import re
from collections import Counter

def analyse_writing_style(samples: list[dict]) -> dict:
    """
    Extract quantitative style features from writing samples.
    These features are injected into the system prompt during training
    to help the model anchor to your specific patterns.
    """
    all_text = [s.get("text", "") for s in samples]
    
    # Sentence-level metrics 
    all_sentences = []
    for text in all_text:
        sents = re.split(r'[.!?]+', text)
        all_sentences.extend([s.strip() for s in sents if s.strip()])
        
    sent_lengths = [len(s.split()) for s in all_sentences]
    avg_sent_len = sum(sent_lengths) / max(len(sent_lengths), 1)
    
    # Word-level metrics 
    all_words = []
    for text in all_text:
        words = re.findall(r"[a-zA-Z']+", text.lower())
        all_words.extend(words)
        
    word_freq = Counter(all_words)
    vocab_size = len(word_freq)
    total_words = len(all_words)
    
    # Filler words & casual markers 
    fillers = ["like", "just", "actually", "basically", "honestly", "literally",
               "yeah", "ah", "oh", "hmm", "haha", "lol", "sure", "right",
               "anyway", "though", "kinda", "gonna", "wanna", "cheers", "mate"]
    filler_counts = {w: word_freq.get(w, 0) for w in fillers if word_freq.get(w, 0) > 0}
    filler_ratio = sum(filler_counts.values()) / max(total_words, 1)
    
    # Formality score (simple heuristic) 
    formal_markers = ["please", "kindly", "regards", "sincerely", "attached",
                      "pursuant", "furthermore", "however", "therefore", "respectively"]
    casual_markers = ["yeah", "lol", "haha", "gonna", "wanna", "nah", "yep",
                      "cool", "dude", "cheers", "mate", "tbh", "imo", "btw"]
                      
    formal_count = sum(word_freq.get(w, 0) for w in formal_markers)
    casual_count = sum(word_freq.get(w, 0) for w in casual_markers)
    
    if formal_count + casual_count > 0:
        formality = formal_count / (formal_count + casual_count) # 0=casual, 1=formal
    else:
        formality = 0.5 # Neutral
        
    # Punctuation habits 
    all_raw = " ".join(all_text)
    uses_ellipsis = all_raw.count("...") > len(all_text) * 0.1
    uses_exclamation = all_raw.count("!") > len(all_text) * 0.2
    uses_lowercase_start = sum(1 for t in all_text if t and t[0].islower()) / max(len(all_text), 1)
    avg_msg_length = sum(len(t.split()) for t in all_text) / max(len(all_text), 1)
    
    style = {
        "total_samples": len(samples),
        "total_words": total_words,
        "vocab_size": vocab_size,
        "avg_sentence_length": round(avg_sent_len, 1),
        "avg_message_length": round(avg_msg_length, 1),
        "formality_score": round(formality, 2), # 0=very casual, 1=very formal
        "top_filler_words": dict(sorted(filler_counts.items(), key=lambda x: -x[1])[:5]),
        "filler_word_ratio": round(filler_ratio, 3),
        "starts_lowercase_pct": round(uses_lowercase_start * 100, 1),
        "uses_ellipsis_often": uses_ellipsis,
        "uses_exclamation_often": uses_exclamation,
    }
    return style

if __name__ == "__main__":
    import json
    # Simple test logic
    print("Testing style analyzer...")
    dummy_samples = [{"text": "yeah honestly i just wanted to grab a coffee"}, {"text": "ah cool mate... cu there!"}]
    print(json.dumps(analyse_writing_style(dummy_samples), indent=2))

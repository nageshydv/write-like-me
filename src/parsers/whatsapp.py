import re
from typing import List, Dict
from .base import BaseParser

class WhatsAppParser(BaseParser):
    """
    Parses WhatsApp chat export text files.
    Extracts messages sent by "my_name" and uses the preceding message as context.
    """
    def __init__(self, my_name: str):
        self.my_name = my_name
        # Matches common WhatsApp export formats:
        # [21/03/24, 18:55:06] Sender: Message
        # 21/03/2024, 18:55 - Sender: Message
        self.pattern = re.compile(r"^(?:\[?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}[,\]] \d{1,2}:\d{2}(?::\d{2})?(?: AM| PM| am| pm)?\]? -? )([^:]+): (.*)")

    def parse(self, filepath: str) -> List[Dict[str, str]]:
        samples = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return []
            
        current_context = "whatsapp chat"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = self.pattern.match(line)
            if match:
                sender, text = match.groups()
                if sender.strip() == self.my_name:
                    samples.append({
                        "text": text.strip(),
                        "context": current_context
                    })
                else:
                    # Preceding message from someone else serves as context
                    current_context = text.strip()
        
        return samples

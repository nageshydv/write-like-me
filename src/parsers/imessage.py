import os
import sqlite3
from typing import List, Dict
from .base import BaseParser

class IMessageParser(BaseParser):
    """
    Parses the local macOS iMessage sqlite database (`chat.db`).
    Extracts messages sent by the user (is_from_me=1) and uses preceding messages as context.
    """
    def parse(self, filepath: str = '~/Library/Messages/chat.db') -> List[Dict[str, str]]:
        filepath = os.path.expanduser(filepath)
        
        # Simple extraction query
        query = """
        SELECT message.text, message.is_from_me
        FROM message
        WHERE message.text IS NOT NULL
        ORDER BY message.date
        """
        samples = []
        try:
            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()
            cursor.execute(query)
            
            context = "imessage chat"
            for row in cursor.fetchall():
                text, is_from_me = row
                if not text:
                    continue
                    
                if is_from_me:
                    samples.append({
                        "text": text,
                        "context": context
                    })
                else:
                    context = text
                    
            conn.close()
        except sqlite3.Error as e:
            print(f"Error reading iMessage DB at {filepath}: {e}")
        
        return samples

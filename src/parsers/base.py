from abc import ABC, abstractmethod
from typing import List, Dict

class BaseParser(ABC):
    """
    Abstract base class for all data parsers.
    Parsers are responsible for reading a raw data export (like WhatsApp, iMessage, etc.)
    and converting it into a list of dictionaries suitable for QLoRA fine-tuning.
    
    Expected output format per list item:
    {
        "text": "The actual message content",
        "context": "Optional context like 'Message to John' or preceding message"
    }
    """

    @abstractmethod
    def parse(self, filepath: str) -> List[Dict[str, str]]:
        """
        Parses the data from the given filepath.
        
        Args:
            filepath (str): Path to the raw export file or database.
            
        Returns:
            List[Dict[str, str]]: A list of parsed message dictionaries.
        """
        pass

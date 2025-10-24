"""Utilities for parsing LLM responses."""

import json
import re
from typing import Optional, Dict, Tuple


class ResponseParser:
    """Parse LLM responses to extract actions and conversational text."""
    
    @staticmethod
    def extract_json(text: str) -> Optional[Dict]:
        """
        Extract JSON object from text.
        
        Args:
            text: Text containing JSON
            
        Returns:
            Parsed JSON dictionary or None
        """
        json_match = re.search(r'\{[^}]+\}', text)
        
        if json_match:
            try:
                json_str = json_match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
        
        return None
    
    @staticmethod
    def extract_conversational_text(text: str) -> str:
        """
        Extract conversational text by removing JSON.
        
        Args:
            text: Full response text
            
        Returns:
            Text without JSON
        """
        return re.sub(r'\{[^}]+\}', '', text).strip()
    
    @staticmethod
    def parse_response(text: str) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Parse response into conversational text and action.
        
        Args:
            text: Full response text
            
        Returns:
            Tuple of (conversational_text, action_dict)
        """
        conversational_text = ResponseParser.extract_conversational_text(text)
        action_dict = ResponseParser.extract_json(text)
        
        return (
            conversational_text if conversational_text else None,
            action_dict
        )
    
    @staticmethod
    def validate_action(action_dict: Dict) -> bool:
        """
        Validate that action dictionary has required fields.
        
        Args:
            action_dict: Parsed action dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if not action_dict:
            return False
        
        required_fields = ["action"]
        return all(field in action_dict for field in required_fields)

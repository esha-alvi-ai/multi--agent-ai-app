import re
import html
class SanitizeValidator:
    def __init__(self,allowed_tags=None,allowed_attrs=None):
        self.allowed_tags=allowed_tags if allowed_tags else []
        self.allowed_attrs=allowed_attrs if allowed_attrs else []
    def sanitize_input(self,text):
        """
        Sanitize the input text by removing disallowed HTML tags and attributes.
        
        Args:
            text (str): The input text to sanitize.
        
        Returns:
            str: The sanitized text.
        """
        if self.allowed_tags:
            text=self._strip_disallowed_tags(text)
        else:
            text=re.sub(r"<[^>]*>","",text)
               # Step 2: Remove dangerous attributes (e.g., onclick, onerror, etc.)
        text = re.sub(r"on\w+\s*=\s*['\"].*?['\"]", "", text, flags=re.IGNORECASE)

        # Step 3: Remove JavaScript: in href or src
        text = re.sub(r"(javascript:)", "", text, flags=re.IGNORECASE)

        # Step 4: Escape HTML special characters (XSS prevention)
        text = html.escape(text)

        # Step 5: Remove multiple spaces and trim
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _strip_disallowed_tags(self, text):
        """
        Removes all tags except allowed ones.
        """
        return re.sub(
            r"</?(?!(" + "|".join(self.allowed_tags) + r")\b)[^>]*>",
            "",
            text
        )

    def is_safe(self, text):
        """
        Checks if the text is safe (no dangerous HTML/JS patterns).
        """
        dangerous_patterns = [
            r"<script.*?>.*?</script>",
            r"on\w+\s*=",
            r"javascript:",
            r"document\.",
            r"window\."
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                return False
        return True
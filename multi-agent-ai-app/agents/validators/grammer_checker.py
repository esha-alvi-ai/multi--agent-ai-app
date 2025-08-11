

import language_tool_python
class  GrammerChecker:
    def __init__(self,language="en-US"):
        self.tool = language_tool_python.LanguageTool(language)
    def check(self,text):
        """
        Check the text for grammar and spelling errors.
        
        Args:
            text (str): The text to check.
        
        Returns:
            list: A list of dictionaries with error details.
        """
        matches = self.tool.check(text)
        errors = []
        for match in matches:
            errors.append({
                "message": match.message,
                "offset": match.offset,
                "length": match.errorLength,
                "context": match.context,
                "replacements": match.replacements
            })
        return errors,matches
    def correct(self, text):
        """
        Correct the text based on grammar and spelling errors.
        
        Args:
            text (str): The text to correct.
        
        Returns:
            str: The corrected text.
        """
        return self.tool.correct(text)
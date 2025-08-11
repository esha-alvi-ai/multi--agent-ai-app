class  LogicValidator:
    def __init__(self,rules=None):
        """
        Initialize the LogicValidator with a set of rules.
        
        Args:
            rules (list, optional): A list of rules to validate against.
        """
        self.rules = rules  if rules  else []
        
    def add_rule(self,rule_func):
        self.rules.append(rule_func)
        
    def validate(self,text):
        """
        Validate the text against the rules.
        
        Args:
            text (str): The text to validate.
        
        Returns:
            bool: True if the text passes all rules, False otherwise.
        """
        falied_rules =[]
        for idx,rule in enumerate(self.rules, start=1):
            try:
                if not rule(text):
                    falied_rules.append(f"Rule {idx} failed.")
            except Exception as e:
                falied_rules.append(f"Rule {idx} raised an exception: {e}")
                
        return {
            "is_valid": len(falied_rules) == 0,
            "failed_rules": falied_rules
        }
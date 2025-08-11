import re
class Refiner:
    def __init__(self):
        pass
    def refine(self,txt:str)->str:
        # Regular expression to match the pattern "## <agent_name> output: <output>"
        text=re.sub(r'\s+','',text).strip()
        sentences=re.split(r'(?<=[.!?]) +', text)
        sentences=[s.capitalize() for s in sentences if s.strip()]
        text = ' '.join(sentences)
        
        text=text.replace(" ,",",")
        text=text.replace(" .",".")
        text=text.replace(" !","!")
        text=text.replace(" ?","?")
        text=text.replace(" ;",";")
        text=text.replace(" :",":")
        
        text=re.sub(r'\b(\w+)\s+\1\b', r'\1', text)  # Remove duplicate words
        if len(text) >200:
            words=text.split()
            formatted=[]
            line=[]
            for w in words:
                line.append(w)
                if len(' '.join(line)) > 80:
                    formatted.append(' '.join(line))
                    line=[]
                    
                if line:
                    formatted.append(' '.join(line))
            text='\n'.join(formatted)
        return text
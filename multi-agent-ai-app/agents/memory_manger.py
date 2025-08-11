from encodings import oem
import time
import uuid
class MemoryManger:
    def __init__(self):
        self.short_term={}
        self.long_term={}
    def  store(self,memory_type,content,tags=None):
        """
        Store content in short-term or long-term memory.
        
        Args:
            memory_type (str): 'short_term' or 'long_term'.
            content (str): The content to store.
            tags (list, optional): Tags associated with the content.
        
        Returns:
            str: Unique identifier for the stored content.
        """
        mem_id = str(uuid.uuid4())
        if memory_type =="short":
            self.short_term[mem_id] = {
                "content": content,
                "timestamp": time.time()
            }
        elif memory_type == "long":
            self.long_term[mem_id] = {
                "content": content,
                "tags": tags or []
            }
        return   mem_id
    def  retrieve(self,memory_type,mem_id):
        """
        Retrieve content from short-term or long-term memory.
        
        Args:
            memory_type (str): 'short_term' or 'long_term'.
            mem_id (str): Unique identifier for the stored content.
        
        Returns:
            dict: The stored content and its metadata, or None if not found.
        """
        if memory_type == "short":
            return self.short_term.get(mem_id)
        elif memory_type == "long":
            return self.long_term.get(mem_id)
        return None
    def update(self,memory_type,mem_id,new_content):
        """
        Update content in short-term or long-term memory.
        
        Args:
            memory_type (str): 'short_term' or 'long_term'.
            mem_id (str): Unique identifier for the stored content.
            new_content (str): The new content to update.
        
        Returns:
            bool: True if updated successfully, False if not found.
        """
        if memory_type == "short" :
            if mem_id in self.short_term:
                self.short_term[mem_id]["content"] = new_content
                return True
        elif memory_type == "long":
            if mem_id in self.long_term:
                self.long_term[mem_id]["content"] = new_content
                return True
        return False
    def delete(self,memory_type,mem_id):
        """
        Delete content from short-term or long-term memory.
        
        Args:
            memory_type (str): 'short_term' or 'long_term'.
            mem_id (str): Unique identifier for the stored content.
        
        Returns:
            bool: True if deleted successfully, False if not found.
        """
        if memory_type == "short":
            return self.short_term.pop(mem_id, None) is not None
        elif memory_type == "long":
            return self.long_term.pop(mem_id, None) is not None
        return False
    
    def search(self,memory_type,keyword):
        """
        Search for content in short-term or long-term memory by keyword.
        
        Args:
            memory_type (str): 'short_term' or 'long_term'.
            keyword (str): Keyword to search for in the content.
        
        Returns:
            list: List of matching content and their identifiers.
        """
        results = []
        if memory_type == "short":
            for mem_id, data in self.short_term.items():
                if keyword.lower() in data["content"].lower():
                    results.append({"id": mem_id, "content": data["content"]})
        elif memory_type == "long":
            for mem_id, data in self.long_term.items():
                if keyword.lower() in data["content"].lower():
                    results.append({"id": mem_id, "content": data["content"], "tags": data.get("tags", [])})
        return results
    def clear_expired_short_term(self,max_age=300):
        """
        Clear short-term memory entries older than max_age seconds.
        
        Args:
            max_age (int): Maximum age of entries in seconds.
        """
        now=time.time()
        to_delete=[
            mem_id for mem_id , data in self.short_term.items()
            if now- data["timestamp"] >max_age
        ]
        for mem_id in to_delete:
            del self.short_term[mem_id]
       
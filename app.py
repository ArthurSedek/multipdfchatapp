'''
    Author: Arthur Sedek
    Email: Arthur.sedek@gmail.com

    DO NOT REMOVE OR MODIFY THE AUTHOR ATTRIBUTION. 
    This attribution acknowledges the efforts of the original developer. 
    Please respect and retain this information when using, modifying, or sharing this code.

    If you have questions or concerns, you're welcome to reach out via the email provided.

'''
from doc_assistant import DocumentAssistant

if __name__ == "__main__":
    assistant = DocumentAssistant("configuration.json")
    assistant.run()

import re
def get_session_id(session_id:str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_id)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""
   
    
  


def get_string_from_dict(pharmacy_item:dict):
    return ", ".join([f"{int(value)} {key}" for key,value in  pharmacy_item.items()])
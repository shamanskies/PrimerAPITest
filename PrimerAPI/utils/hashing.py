import hashlib

def unique_name_from_str(string: str, last_idx: int = 12) -> str:
    """
    Generates a unique id name
    refs:
    - md5: https://stackoverflow.com/questions/22974499/generate-id-from-string-in-python
    - sha3: https://stackoverflow.com/questions/47601592/safest-way-to-generate-a-unique-hash
    (- guid/uiid: https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python?noredirect=1&lq=1)
    """
    m = hashlib.md5()
    string = string.encode('utf-8')
    m.update(string)
    unqiue_name: str = str(int(m.hexdigest(), 16))[0:last_idx]
    return unqiue_name
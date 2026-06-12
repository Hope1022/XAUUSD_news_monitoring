import hashlib

def hashing(title):
    return hashlib.sha256(title.encode()).hexdigest()


    

import hashlib

# db = get_db() # or simply db = sessionLocal()

def hashing(title):
    return hashlib.sha256(title.encode()).hexdigest()


    
import hashlib
import mimetypes

def get_mime(path: str) -> str:
    try:
        type = mimetypes.guess_type(path, strict=True)
        if type:
            return type[0]
        else:
            return 'application/octet-stream'
    except:
        return 'application/octet-stream'

def hash_str(*args) -> str:
    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''

def safe_list(extra, key, default='') -> str:
    extra = dict(extra)
    
    try:
        value = extra.get(key, [default])
        return value[0] if value else default
    except:
        return ''

import string
allowed_key_characters = set( string.ascii_letters + string.digits + '.' )
def safety_filter(c):
    return c in allowed_key_characters

def get_filename( filename ):
    """get a clean, safe key from whatever 'filename' the client gave us"""
    filename = unicode(filename)
    filename_index=max(filename.rfind('/'), filename.rfind('\\') ) +1
    basename = filename[filename_index:]
    clean_filename =  filter( safety_filter, basename )
    

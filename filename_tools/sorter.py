import re
import os.path

convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

def sort_nicely( l, filename=False):
    """ Sort the given list in the way that humans expect.
    
    Params:
    filename=True: Try to split of directory from string and sort on filenames
    """
    if filename:
        l.sort( key=lambda key: alphanum_key(os.path.basename(key)) )
    else:
        l.sort( key=alphanum_key )
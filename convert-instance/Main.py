from optparse import OptionParser
from code.Convert import *
import os

if __name__ == "__main__":
    parser = OptionParser()
    
    parser.add_option('-u', '--unique', dest="file")
    parser.add_option('-a', '--all', dest="root")
    (opts, _) = parser.parse_args()
    path = opts.file
    root = opts.root
    if path is not None:
        inst = Convert(path)
        inst.to_string()
        inst.write_file("text")
    elif root is not None:
        for (_, _, paths) in os.walk(root):
            for path in paths:
                inst = Convert(os.path.join(root + path))
                inst.to_string()
                inst.write_file(f"{path}_conv")
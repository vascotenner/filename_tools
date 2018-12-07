'''

Published under GPL license
(c) Vasco Tenner 2013
'''
import os
import glob
import re
from . import sorter

zeros_default = 3


def find_available_filename(base, extension='', start=1, zeros=zeros_default,
                            prefix=True, fmt='{:0{zeros}d}', recursive=True):
    """ Find the first filename that not exists """
    number = find_available_number(start=start, zeros=zeros, fmt=fmt,
                                   recursive=recursive)
    name = create_name(base, extension, number, prefix)
    return name


def create_name(base, ext, i, prefix=True):
    # i = string. number of zeros is controlled elsewhere
    if prefix:
        return '{i}{base}.{ext}'.format(i=i, base=base, ext=ext)
    else:
        return '{base}{i}.{ext}'.format(i=i, base=base, ext=ext)


def find_available_number(start=1, zeros=zeros_default, fmt='{:0{zeros}d}',
                          recursive=True):
    try:
        newnr = len(Files(min_digits=zeros, recursive=recursive).files())
    except ValueError:
        newnr = 0

    if newnr == 0:
        return fmt.format(start, zeros=zeros)
    else:
        nr = max([newnr, start])
        if nr > 10**zeros-1:
            print('First free number to high, adding extra digit')
            return fmt.format(nr, zeros=zeros+1)
        else:
            return fmt.format(nr, zeros=zeros)


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if re.match(pattern, basename):
                filename = os.path.join(root, basename)
                yield filename


def files(directory='.', recursive=True, ignore=None):
    return Files(directory=directory, recursive=recursive, ignore=ignore
                 ).files()


def filenumber(f):
    '''Get the first numbers from a filename'''
    return sorter.alphanum_key(os.path.basename(f))[1]


def filebase(f):
    '''Get the base string from a filename'''
    return os.path.splitext(os.path.basename(f))[0].split('_', maxsplit=1)[1]


class Files(object):
    ''' Create a list with files[i] = "i_*"\

    params:
    directory: starting dir
    recursive: walk through all sub directories
    ignore: list of glob_pattern of files that should be ignored
    min_digits - max_digits: minimum and maxium digits in front of filename '''
    def __init__(self, directory='.', recursive=True, ignore=None,
                 min_digits=2, max_digits=4, filename_spec='\d{%i,%i}_'):
        self.directory = directory
        self.recursive = recursive
        self.ignore = [] if ignore is None else ignore
        self.min_digits = min_digits
        self.max_digits = max_digits
        self.filename_spec = filename_spec

    def files(self):
        '''Return a list of files'''

        filename_pattern = self.filename_spec % (self.min_digits,
                                                 self.max_digits)
        if self.recursive:
            files = list(find_files(self.directory,
                                    filename_pattern))
        else:
            files = [f for f in os.listdir(self.directory)
                     if (os.path.isfile(os.path.join(self.directory, f)) and
                         re.match(filename_pattern, f)
                         )
                     ]

        # apply ignores
        files = [f for f in files if not any([glob.fnmatch.fnmatch(f, ign)
                                              for ign in self.ignore])]
        sorter.sort_nicely(files, filename=True)
        # Create an array with files, where the index is the file number
        files2 = {filenumber(f): f
                  for f in files}
        max_filenr = max(files2.keys()) if (len(files2.keys()) > 0) else 0
        files = [files2.get(i, None) for i in range(max_filenr + 1)]
        return files

    def __getitem__(self, key):
        return self.files()[key]

    def items(self):
        return enumerate(self)

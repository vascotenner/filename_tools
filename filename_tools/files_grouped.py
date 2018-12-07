####
#
# Tools to get keywords and values from filenames and to group according
# to them
#
# (c) Vasco Tenner 2018
#
# Available under GPL licence
#
####

import os
import collections


def extract_keywords(fname):
    ''' Extract keyword=value from filename'''
    # remove extension
    fname = os.path.splitext(fname)[0]
    parts = os.path.basename(fname).split('_')
    keywords = {}
    for part in parts:
        try:
            key, value = part.split('=')
            keywords[key] = value
        except ValueError:
            keywords[part] = None
    return keywords


def get_unique_values(files, keyword='axisz'):
    '''Get unique values for a certain keyword'''
    values = set()
    for f in files:
        try:
            values.add(extract_keywords(f)[keyword])
        except IndexError:
            pass
    return values


def group_file_list_by_filename(files, keyword='axisz'):
    '''Gets a group of files with the same keyword=value in their filename'''
    filelists = collections.OrderedDict()
    for f in files:
        try:
            val = extract_keywords(f)[keyword]
            if val not in filelists:
                filelists[val] = []
            filelists[val].append(f)
        except IndexError:
            pass
    return filelists


def move_grouped_files(filelists, keyword, verbose=True):
    '''Create a directory with name "keyword=filelist.key()" and move
    files of that group to it

    Example:
    import find_available_filenames
    files = find_available_filenames.Files()
    filelists = group_file_list_by_filename(files, keyword='axisz')
    move_grouped_files(filelists, keyword='axisz')
    '''
    dirs = []
    files = []
    for key, filelist in filelists.items():
        # Get deepest subdir
        subdir = os.path.dirname(filelist[0])
        pathspec = '{}/{}={}'.format(subdir, keyword, key)
        try:
            os.makedirs(pathspec)
            dirs.append(pathspec)
        except FileExistsError:
            pass
        for f in filelist:
            os.rename(f, '{}/{}'.format(pathspec, os.path.basename(f)))
            files.append(f)
    if verbose:
        print('Created {} dirs'.format(len(dirs)))
        print('Moved {} files'.format(len(files)))

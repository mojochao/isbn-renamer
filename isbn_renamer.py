"""isbn_renamer.py

Usage:
  isbn_renamer.py [options] FILE

Options:
  -b    Keep backup file with original file name

"""
import argparse
import os
import re
import shutil

import isbnlib


isbn10_regex = re.compile(r'.*(\d{9}[\d|X]).*')
rename_template = '{title}, {publisher}, {year}{ext}'


def fetch_metadata(obj):
    isbn = obj.get('isbn')
    if isbn:
        meta = isbnlib.meta(isbn)
        result = dict(obj)
        result['title'] = meta['Title']
        result['publisher'] = meta['Publisher']
        result['year'] = meta['Year']
        return result
    else:
        return obj


def rename_file(obj, backup=False):
    src = obj['filename']
    _, ext = os.path.splitext(src)
    dst = rename_template.format(title=obj['title'], publisher=obj['publisher'], year=obj['year'], ext=ext)
    if backup:
        shutil.copyfile(src, src + '.bak')
    os.rename(src, dst)
    print('{} renamed to {}'.format(src, dst))
    result = dict(obj)
    result['rename'] = dst
    return result


def extract_isbn(filename):
    match = isbn10_regex.search(filename)
    return {"filename": filename, "isbn": match.group(1) if match else None}


def main():
    parser = argparse.ArgumentParser(description='rename file with isbn number to human representation')
    parser.add_argument('-b', '--backup', action='store_true', help='keep backup of original file name')
    parser.add_argument('files', nargs='+', metavar='FILE', help='file containing isbn number in file name')
    args = parser.parse_args()

    isbn_nums = [extract_isbn(f) for f in args.files]
    fetched_metadata = [fetch_metadata(n) for n in isbn_nums if n is not None]
    _ = [rename_file(f) for f in fetched_metadata]


if __name__ == '__main__':
    main()

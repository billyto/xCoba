__author__ = 'Billy Tobon'

import os
import re
import argparse


parser = argparse.ArgumentParser(description='Find unused images on an xcode project.')
parser.add_argument('path', help='Project path')

args = parser.parse_args()
print(args.path)

path = args.path
_digits = re.compile('\d')


def contains_digits(d):
    return bool(_digits.search(d))


assets_list = []
source_list = []
unused = []

for dirname, dirnames, filenames in os.walk(path):

    # print path to all filenames.
    for filename in filenames:
        if filename.endswith(".png") or filename.endswith(".jpg"):
            path_to_file = os.path.join(dirname, filename)
            clean_name = filename.split('.')[0]
            if not '@2x' in clean_name:
                assets_list.append(clean_name)

        if filename.endswith(".m") or filename.endswith(".plist") or filename.endswith(".xib"):
            path_to_file = os.path.join(dirname, filename)
            source_list.append(path_to_file)

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')

    if '3rdParty' in dirnames:
        dirnames.remove('3rdParty')

for image in assets_list:
    is_used = False
    objcImage = '@"' + image

    for source_file in source_list:
        f = open(source_file)
        content = f.read()
        f.close()
        image_to_search = objcImage if source_file.endswith('.m') else image

        if not content.find(image_to_search) == -1:
            is_used = True
            break

        if contains_digits(image_to_search):
            numbers = re.search('[0-9]+', image_to_search)
            img = re.sub(r'\d+', '%d', image_to_search)

            if not content.find(img) == -1:
                is_used = True
                break

    if not is_used:
        unused.append(image)

print '%d unused images found' % len(unused)

for image in unused:
    print '* %s' % image

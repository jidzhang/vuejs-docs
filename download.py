#!/usr/env/bin python
# -*- coding:utf-8 -*-

import os, sys, re, urllib2


def download(path, ext):
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        for f in subfile:
            subf = os.path.join(dirname, f)
            if subf.endswith(ext):
                fix_file(subf)
        for f in subdir:
            subf = os.path.join(dirname, f)
            download(subf, ext)


def fix_file(path):
    with open(path, 'r+') as f:
        data = f.read()
        found = False
        pat = r'="(https?:)?//([^"<]*\.(js|css|svg))"'
        itr = re.finditer(pat, data)
        for match in itr:
            pre = match.group(1)
            if not pre:
                pre = 'https:'
            url = match.group(2)
            parts = url.split('/')
            n = len(parts)
            filename = parts[n - 1]
            dl_dir = 'dl/'
            for i in range(n - 1):
                dl_dir = dl_dir + parts[i] + '/'
            if not os.path.exists(dl_dir):
                os.makedirs(dl_dir)
            dl_file = dl_dir + filename
            downloaded = False
            if not os.path.exists(dl_file):
                try:
                    print('download from: ' + pre + '//' + url)
                    print('download to: ' + dl_file)
                    response = urllib2.urlopen(pre + '//' + url)
                    html = response.read()
                    with open(dl_file, 'w+') as df:
                        df.write(html)
                        downloaded = True
                except:
                    print("download failed: " + pre + '//' + url)
            else:
                downloaded = True
            if downloaded:
                if re.search(pat, data) != None:
                    data = re.sub(pat, r'="/dl/\2"', data)
                    found = True

        if found:
            f.seek(0)
            f.truncate()
            f.write(data)


if __name__ == '__main__':
    download('./themes', '.ejs')
    download('./src/v2', '.md')

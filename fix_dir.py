#!/usr/env/bin python
#-*- coding:utf-8 -*-

import os,sys,re,glob

def replace_by_dir(path, depth):
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        for f in subfile:
            subf = os.path.join(dirname, f)
            if subf.endswith('.html'):
                repalce_in_file(subf, depth)
        for f in subdir:
            subf = os.path.join(dirname, f)
            replace_by_dir(subf, depth + 1)

def repalce_in_file(path, depth):
    dots = ''
    if (depth > 0):
        dots = '../' * depth
    with open(path, 'r+') as f:
        data = f.read()
        found = False
        # pat = r'src=".*?/fastclick.min.js"'
        # if (re.search(pat, data) != None):
        #     data = re.sub(pat, r'src="https://cdn.bootcss.com/fastclick/1.0.6/fastclick.min.js"', data)
        #     found = True
        pat = r'(href|src)="//'
        if (re.search(pat, data) != None):
            data = re.sub(pat, r'\1="http://', data)
            found = True
        pat = r'(href|src|content)="/([^/])'
        if (re.search(pat, data) != None):
            data = re.sub(pat, r'\1="' + dots + r'\2', data)
            found = True
        pat = r'(href=".+?)/"'
        if (re.search(pat, data) != None):
            data = re.sub(pat, r'\1/index.html"', data)
            found = True
        pat = r'<div id="ad">.*?</div>'
        if (re.search(pat, data, re.S) != None):
            data = re.sub(pat, '', data, flags=re.S)
            found = True
        # pat = r'\starget="_blank"'
        # if (re.search(pat, data) != None):
        #     data = re.sub(pat, '', data)
        #     found = True
        pat = r'<script>[^<]*google-analytics\.com[^<]*</script>'
        if (re.search(pat, data, re.S) != None):
            data = re.sub(pat, '', data, flags=re.S)
            found = True
        if found:
            f.seek(0)
            f.truncate()
            f.write(data)

def fix_css_url():
    path = os.path.expanduser('./css')
    for (dirname, subdir, subfile) in os.walk(path):
        for f in subfile:
            subf = os.path.join(dirname, f)
            if subf.endswith('.css'):
                with open(subf, 'r+') as f:
                    data = f.read()
                    found = False
                    pat = r'(url\(")/([^/])'
                    if (re.search(pat, data) != None):
                        data = re.sub(pat, r'\1../\2', data)
                        found = True
                    if found:
                        f.seek(0)
                        f.truncate()
                        f.write(data)
def fix_service_worker():
    p = './service-worker.js'
    with open(p, 'r+') as f:
        data = f.read()
        found = False
        pat = r'"/([^/].*?)"'
        if (re.search(pat, data) != None):
            data = re.sub(pat, r'"\1"', data)
            found = True
        if found:
            f.seek(0)
            f.truncate()
            f.write(data)



if __name__ == '__main__':
    replace_by_dir('.', 0)
    fix_css_url()
    fix_service_worker()
#!/usr/env/bin python
#-*- coding:utf-8 -*-

import os,sys,re,glob

def pre_fix(path):
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        for f in subfile:
            subf = os.path.join(dirname, f)
            if subf.endswith('.ejs'):
                fix_file(subf)
        for f in subdir:
            subf = os.path.join(dirname, f)
            pre_fix(subf)

def fix_file(path):
    with open(path, 'r+') as f:
        data = f.read()
        found = False
        #删除单行
        patns = []
        patns.append(r'<meta.*?browserconfig.xml">')
        patns.append(r'<link .*?manifest.json">')
        patns.append(r"<%- partial\('partials/ad(-text)?'\) %>")
        patns.append(r"<%- partial\('partials/sponsors_sidebar'\) %>")
        for pat in patns:
            if (re.search(pat, data) != None):
                data = re.sub(pat, '', data)
                found = True
        #删除多行
        patns = []
        patns.append(r'<!--\s*ga\s*-->\n\s*<script>.*?google-analytics.com.*?</script>')
        patns.append(r'<div class="footer">.*?</div>')
        patns.append(r'<select class="version-select">.*?</select>')
        for pat in patns:
            if (re.search(pat, data, re.S) != None):
                data = re.sub(pat, '', data, flags=re.S)
                found = True
        #replace
        pat = r'<%- url_for\("/js/vue.js"\) %>'
        if (re.search(pat, data) != None):
            data = re.sub(pat, r'<%- url_for("/js/vue.min.js") %>', data)
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
    pre_fix('./themes')

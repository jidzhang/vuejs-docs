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
        patns.append(r'<link href=.//fonts.googleapis.com/css.*?>')
        # patns.append(r'\starget="_blank"');
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
                print('delete google-analytics')
                data = re.sub(pat, '', data, flags=re.S)
                found = True
        #replace vue.js
        pat = r'<%- url_for\("/js/vue.js"\) %>'
        if (re.search(pat, data) != None):
            print('replace vue.js with vue.min.js')
            data = re.sub(pat, r'<%- url_for("/js/vue.min.js") %>', data)
            found = True

        if found:
            f.seek(0)
            f.truncate()
            f.write(data)


if __name__ == '__main__':
    """
    删除无用标签
    """
    pre_fix('./themes')

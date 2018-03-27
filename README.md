# vuejs2hbuilder

把[Vue.js](http://cn.vuejs.org)官方文档转成app，方便随时查看和学习。

Vue.js官方文档是学习vuejs的最好书籍，没有之一。

## usage

```
rm -Rf build/
git clone --depth 1 https://github.com/vuejs/cn.vuejs.org build
cd build/
rm -rf public/
npm i
npm run build
cp ../pre_fix.py .
python pre_fix.py
cp ../fix_dir.py public/
cd public
python fix_dir.py
```
# rm -Rf build/
# git clone --depth 1 https://github.com/vuejs/cn.vuejs.org build
cd build/
rm -rf public/
npm i
npm run build
cp ../pre_fix.py .
python pre_fix.py
cp ../fix_dir.py public/
cd public
python fix_dir.py
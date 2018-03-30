# rm -Rf build/
# git clone --depth 1 https://github.com/vuejs/cn.vuejs.org build
cd build/
rm -rf public/
cp ../pre_fix.py .
cp ../download.py .
python pre_fix.py
python download.py
npm install
npm run build
cp -r dl public
cp ../fix_dir.py public/
cd public
python fix_dir.py
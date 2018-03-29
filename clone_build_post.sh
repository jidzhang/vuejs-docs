#!/bin/bash

work_dir=$(pwd)
reps[0]='https://github.com/vuejs/vuejs.org.git'
reps[1]='https://github.com/vuejs/cn.vuejs.org.git'
reps[2]='https://github.com/vuejs/jp.vuejs.org.git'
reps[3]='https://github.com/translation-gang/ru.vuejs.org.git'
reps[4]='https://github.com/vuejs-kr/kr.vuejs.org.git'
reps[5]='https://github.com/vuejs-br/br.vuejs.org.git'
reps[6]='https://github.com/vuejs-fr/vuejs.org.git'
reps[7]='https://github.com/vuejs-vn/vuejs.org.git'
langs[0]='en'
langs[1]='cn'
langs[2]='jp'
langs[3]='ru'
langs[4]='kr'
langs[5]='br'
langs[6]='fr'
langs[7]='vi'
length=${#reps[*]}
cd vuejs.org
for ((i=0; i<$length; i++))
do
	lang="${langs[$i]}"
	rep="${reps[$i]}"
	if [ ! -e $lang ]; then
		echo "git clone $rep $lang"
		# git clone --depth 1 $rep $lang
	else
		echo "git reset --hard origin; git pull"
		# cd $lang; git reset --hard origin; git pull; cd ..
	fi
	if [ -e $lang ]; then
		cd $lang
		cp $work_dir/download.py .
		cp $work_dir/pre_fix.py .
		if [ ! -d themes/vue/source/fonts ]; then
			echo 'fix google-fonts'
			cp -r $work_dir/font-fix/fonts themes/vue/source
			cp $work_dir/font-fix/_fonts.styl themes/vue/source/css
		fi
		# echo "cd $lang; download js/css/font..."
		# python pre_fix.py
		# python download.py
		# npm install
		#if [ $lang = 'kr' ]; then
		#	npm run deploy
		#else
		#	npm run build
		#fi
		# rm -rf node_modules
		#cp -R dl public/dl
		cp $work_dir/fix_dir.py ./public; cd public
		python fix_dir.py
		cd ..
		echo "post to $work_dir/www/html/vuejs.org/$lang"
		cp -R public $work_dir/www/html/vuejs.org/$lang
		cd ..
	fi
done

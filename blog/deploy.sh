
rm -rf public

cd repository && git pull --rebase

cd blog && hugo --minify -d ../../public

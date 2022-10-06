
rm -rf public

cd repository && git submodule init && git submodule update && git pull --rebase

cd blog && hugo --minify -d ../../public

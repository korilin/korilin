#!/bin/bash

git pull --rebase && git submodule init && git submodule update

rm -rf public

cd blog && hugo --minify -d ../public

cd ..

#!/bin/bash

rm -rf public

cd repository && git pull --rebase && git submodule init && git submodule update

cd blog && hugo --minify -d ../public

cd ..

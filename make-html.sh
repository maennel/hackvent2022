#!/usr/bin/env bash
set -e

mkdir -p build/md/
mkdir -p build/static/
rm -rf build/md/*
rm -rf build/static/*

find ./dec* ./hidden* -iname dec??.md -or -iname hidden??.md > build/.files.tmp
echo "./hv22.md" >> build/.files.tmp

cp -f $(cat build/.files.tmp) build/md/

STATIC_FILES=$(cat build/md/* | grep -oe '(./[^)]*)' | tr -d "()" | sed 's#^./##')
for f in ${STATIC_FILES}; do
    find ./dec* ./hidden* -name ${f} -exec cp -f {} build/static/ \;
done

rm -f build/main.md
cat build/md/hv22.md | sed 's#](./#](./static/#g' > build/main.md
cat build/md/dec* | sed 's#](./#](./static/#g' | sed 's/^#/##/g' >> build/main.md
cat build/md/hidden* | sed 's#](./#](./static/#g' | sed 's/^#/##/g' >> build/main.md

# TODO: Convert to html either via https://markdowntohtml.com/ or via Github.
rm -rf public/
mkdir -p public/static/
cp build/main.md public/
cp build/static/* public/static/

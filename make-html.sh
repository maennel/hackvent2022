#!/usr/bin/env bash
set -e

mkdir -p build/md/
rm -rf build/md/*

find ./dec* ./hidden* -iname dec??.md -or -iname hidden??.md > build/.files.tmp
echo "./hv22.md" >> build/.files.tmp

cp -f $(cat build/.files.tmp) build/md/

for mdf in $(find ./dec* ./hidden* -iname dec??.md -or -iname hidden??.md); do
    d=$(dirname $mdf)
    build_d=build/md
    for sf in $(grep -oe '(./[^)]*)' ${mdf} | tr -d "()"); do
        # Relative path from public/main.md to decXX/file.ext
        rp=".$d/$(basename $sf)"
        # echo "$mdf: $sf - $rp"
        sed -i "s#$sf#$rp#g" "$build_d/$(basename $mdf)"
    done
done

rm -f build/main.md

# Compose main.md file
cat build/md/hv22.md > build/main.md
cat build/md/dec* | sed 's/^#/##/g' >> build/main.md
cat build/md/hidden* | sed 's/^#/##/g' >> build/main.md

# Create table of contents of all second level headers starting with a "["
grep '^##[^#]\[.*' build/main.md | sed 's/## //g' > build/md/.headers
cat build/md/.headers | tr "A-Z\ " "a-z\-" | tr -cd "a-z0-9\-\n" | sed 's/^/#/g' > build/md/.links
paste build/md/.headers build/md/.links | sed 's/^/- [/g' | sed 's/\t/](/g' | sed 's/$/)/g' > build/md/.toc
sed -i '/<TOC>/{r build/md/.toc
              d}' build/main.md


# TODO: Convert to html either via https://markdowntohtml.com/ or via Github.
rm -rf public/
mkdir -p public/
cp build/main.md public/

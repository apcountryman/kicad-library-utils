#!/bin/bash

# example usage
# in the kicad-symbols dir:
# # EXPORT FOOTPRITNS_DIR="../kicad-footprints/"
# # ../kicad-library-utils/tools/diff_symbols.sh d694681f0b2dee188845e8e4add5a8dcefb9eae2

if [ -z $FOOTPRINTS_DIR ]; then
  FOOTPRINTS_DIR=../kicad-footprints
fi

if [ -z $1 ]; then
  TARGET_SHA="HEAD"
else
  TARGET_SHA=$1
fi

if [ -z $BASE_SHA ]; then
  BASE_SHA="$TARGET_SHA~1"
fi

CI_BUILDS_DIR=`mktemp -d`


# get the list of files we want to compare
echo "Comparing range $BASE_SHA to $TARGET_SHA"
LIBS_NEW=$(git diff-tree --diff-filter=AMR --no-commit-id --oneline --name-only -r "$BASE_SHA" "$TARGET_SHA" | grep '\.kicad_sym$') #| sed -e "s#^#$CI_PROJECT_DIR/#;")
LIBS_OLD=$(git diff-tree --diff-filter=DMR --no-commit-id --oneline --name-only -r "$BASE_SHA" "$TARGET_SHA" | grep '\.kicad_sym$')

# do some debug output
echo "Found new Libraries: $LIBS_NEW"
echo "Found old Libraries: $LIBS_OLD"

# checkout the previous version of the 'old' files so we can compare against them
mkdir -p $CI_BUILDS_DIR/kicad-symbols-prev
for LIBNAME in $LIBS_OLD; do
  git cat-file blob "$BASE_SHA:$LIBNAME" > "$CI_BUILDS_DIR/kicad-symbols-prev/$LIBNAME"
done

mkdir -p $CI_BUILDS_DIR/kicad-symbols-curr
for LIBNAME in $LIBS_NEW; do
  git cat-file blob "$TARGET_SHA:$LIBNAME" > "$CI_BUILDS_DIR/kicad-symbols-curr/$LIBNAME"
done

# now run comparelibs
`dirname $0`/../klc-check/comparelibs.py -v --old $CI_BUILDS_DIR/kicad-symbols-prev/* --new $CI_BUILDS_DIR/kicad-symbols-curr/* --check --check-derived --footprint_directory $FOOTPRINTS_DIR -m

rm -rf $CI_BUILDS_DIR

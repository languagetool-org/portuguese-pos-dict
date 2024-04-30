#!/usr/bin/env bash
# Shell script to check if all .dic and .aff files are encoded in ISO-8859-1

get_encoding() {
  for ext in dic aff; do
    find ./data/spelling-dict/hunspell -type f -name "pt*.${ext}" -exec file {} \;
  done
}

FILE_ENCODINGS=$(get_encoding)

check_encoding() {
  echo "${FILE_ENCODINGS}" | grep -v "ISO-8859 text"
}


if [[ -z $(check_encoding) ]]; then
  echo "All .dic and .aff files are encoded in ISO-8859-1, we're good!"
  exit 0
else
  echo "Some .dic and .aff files are not encoded in ISO-8859-1, please fix this."
  echo "${FILE_ENCODINGS}"
  exit 1
fi
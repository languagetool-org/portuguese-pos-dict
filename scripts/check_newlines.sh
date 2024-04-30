#!/usr/bin/env bash

# Check for files that do not end with a newline

check_newlines() {
  find ./data/src-dict -name "*.txt" -type f -print0 | xargs -0 -n1 bash -c 'tail -c1 "$1" | read -r _ || echo "$1"' bash
}

NO_NEWLINE_FILES=$(check_newlines)

if [[ -z "${NO_NEWLINE_FILES}" ]]; then
  echo "All files end with a blank line, which is good."
  exit 0
else
  echo "Some files do not end with a newline:"
  echo "${NO_NEWLINE_FILES}"
  exit 1
fi

#!/bin/bash

# Calling this shell script directly will result in an error, and that is BY DESIGN. Please call the Python wrapper
# instead, so all the environment variables are set and, at the end, the dictionary plaintext is actually compiled into
# the appropriate binaries!

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${SOURCE_DIR}/prepare.sh"

check_requirements

# Make sure 'results/lt' dir exists
mkdir -p "$RESULTS_DIR"

#cd "$DATA_SRC_DIR" || exit
#./sort-all.sh
cd "$REPO_DIR" || exit

rm "$RESULTS_DIR"/*.txt

function sed_cmd {
  _expr="$1"
  _filepath=$2
  if [[ "$OS" == "Darwin" ]]; then
    sed -i '' -E "$_expr" "$_filepath"
  else
    sed -i -E "$_expr" "$_filepath"
  fi
}

for pos in "nouns" "adjectives"; do
  echo "${pos}: FDIC to LT..."
  perl "${FDIC_DIR}/flexiona.pl" "${DATA_SRC_DIR}/${pos}-fdic.txt" "${RESULTS_DIR}/${pos}-lt.txt"
done

echo "verbs: FDIC to LT..."
perl "${FDIC_DIR}/conjuga-verbs.pl" "${DATA_SRC_DIR}/verbs-fdic.txt" "${RESULTS_DIR}/verbs-lt.txt" "${DATA_SRC_DIR}/models-verbals/"

echo "remaining POS..."
OTHERS_LT_PATH="${RESULTS_DIR}/others-lt.txt"
cat "$DATA_SRC_DIR"/*-lt.txt > "$OTHERS_LT_PATH"

echo "Cleaning up files..."
echo "... removing comments..."
sed_cmd 's/ *#.*$//' "$OTHERS_LT_PATH"
echo "... removing trailing whitespaces..."
sed_cmd 's/\s+$//' "$OTHERS_LT_PATH"
echo "... removing blank lines..."
sed_cmd '/^$/d' "$OTHERS_LT_PATH"
echo "... replacing single whitespaces with tabs..."
for pos in "nouns" "adjectives" "verbs"; do
  sed_cmd 's/ /\t/g' "${RESULTS_DIR}/${pos}-lt.txt"
done

cat "$RESULTS_DIR"/*-lt.txt > "$RESULT_DICT_FILEPATH"
rm "$RESULTS_DIR"/*-lt.txt

# Sort
export LC_ALL=C && sort -u "$RESULT_DICT_FILEPATH" > "$SORTED_DICT_FILEPATH"
rm "$RESULT_DICT_FILEPATH"
mv "$SORTED_DICT_FILEPATH" "$RESULT_DICT_FILEPATH"

if [[ -f "$OLD_DICT_FILEPATH" ]]; then
  diff "$OLD_DICT_FILEPATH" "$RESULT_DICT_FILEPATH" > "$DICT_DIFF_FILEPATH"
  echo "Diff results in folder ${DICT_DIFF_FILEPATH}"
  grep "ERROR" "$RESULT_DICT_FILEPATH"
  git --no-pager diff --no-index "$OLD_DICT_FILEPATH" "$RESULT_DICT_FILEPATH"
fi

echo "DONE!"
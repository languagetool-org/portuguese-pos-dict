#!/bin/bash

# Hacky workaround to make sure we're at the top of the repo, since there's a bunch of hardcoded relative paths here.

if [[ ! -d ".git" ]]; then
  echo "You are not at the top of the repo: ${PWD}."
  echo "Move to the top and try again."
  exit 1
fi

function check_perl_pkg_installed {
  if [[ ! $(perldoc -l "${1}") ]]; then
    echo "The Perl scripts will need '${1}'. Please use cpan to install it and try again."
    exit 2
  fi
}

for pkg in "Switch" "Text::Unaccent::PurePerl"; do
  check_perl_pkg_installed $pkg
done

# Detect the operating system so we pick the right sed.
OS="$(uname)"
START_DIR=$PWD
DATA_SRC_DIR="${START_DIR}/data/src-dict"
RESULTS_DIR="${START_DIR}/results/lt"
FDIC_DIR="${START_DIR}/fdic-to-lt"
RESULT_DICT_FILEPATH="${RESULTS_DIR}/dict.txt"
SORTED_DICT_FILEPATH="${RESULTS_DIR}/dict_sorted.txt"
DICT_DIFF_FILEPATH="${RESULTS_DIR}/dict.diff"
OLD_DICT_FILEPATH="${RESULTS_DIR}/dict.old"

# Make sure 'results/lt' dir exists
mkdir -p "$RESULTS_DIR"

cd "$DATA_SRC_DIR" || exit
./sort-all.sh
cd "$START_DIR" || exit

rm "$RESULTS_DIR"/*.txt

echo "Nouns: FDIC to LT..."
perl "${FDIC_DIR}/flexiona.pl" "${DATA_SRC_DIR}/nouns-fdic.txt" "${RESULTS_DIR}/nouns-lt.txt"

echo "Adjectives: FDIC to LT..."
perl "${FDIC_DIR}/flexiona.pl" "${DATA_SRC_DIR}/adjectives-fdic.txt" "${RESULTS_DIR}/adjectives-lt.txt"

echo "Verbs: FDIC to LT..."
perl "${FDIC_DIR}/conjuga-verbs.pl" "${DATA_SRC_DIR}/verbs-fdic.txt" "${RESULTS_DIR}/verbs-lt.txt" "${DATA_SRC_DIR}/models-verbals/"

echo "Remaining categories..."
cat "$DATA_SRC_DIR"/*-lt.txt > "${RESULTS_DIR}/others-lt.txt"

echo "Removing comments..."
if [[ "$OS" == "Darwin" ]]; then
    sed -i '' 's/ *#.*$//' "$RESULTS_DIR/others-lt.txt"
    sed -i '' -E 's/\s+$//' "$RESULTS_DIR/others-lt.txt"
    sed -i '' '/^$/d' "$RESULTS_DIR/others-lt.txt"
else
    sed -i 's/ *#.*$//' "$RESULTS_DIR/others-lt.txt"
    sed -i -E 's/\s+$//' "$RESULTS_DIR/others-lt.txt"
    sed -i '/^$/d' "$RESULTS_DIR/others-lt.txt"
fi

cat "$RESULTS_DIR"/*-lt.txt > "$RESULT_DICT_FILEPATH"
rm "$RESULTS_DIR"/*-lt.txt

# sort
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
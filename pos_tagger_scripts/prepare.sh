#!/bin/bash

REQUIRED_PACKAGES=("Switch" "Text::Unaccent::PurePerl")

function check_perl_installed {
  if [[ ! $(which perl) ]]; then
    echo "You don't have Perl installed! Please install it and try again."
    exit 1
  fi
}

function check_perl_pkg_installed {
  if [[ ! $(perldoc -l "${1}") ]]; then
    echo "The Perl scripts will need '${1}'. Please use cpan to install it and try again."
    exit 2
  fi
}

function check_requirements {
  check_perl_installed
  for pkg in "${REQUIRED_PACKAGES[@]}"; do
    check_perl_pkg_installed "$pkg"
  done
}

# Detect the operating system so we pick the right sed.
OS="$(uname)"
export OS
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$( dirname "$THIS_DIR")"
export REPO_DIR
export SCRIPTS_DIR=$THIS_DIR
export DATA_SRC_DIR="${REPO_DIR}/data/src-dict"
export RESULTS_DIR="${REPO_DIR}/results/lt"
export FDIC_DIR="${SCRIPTS_DIR}/fdic-to-lt"
export RESULT_DICT_FILEPATH="${RESULTS_DIR}/dict.txt"
export SORTED_DICT_FILEPATH="${RESULTS_DIR}/dict_sorted.txt"
export DICT_DIFF_FILEPATH="${RESULTS_DIR}/dict.diff"
export OLD_DICT_FILEPATH="${RESULTS_DIR}/dict.old"

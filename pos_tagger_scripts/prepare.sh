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

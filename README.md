[![Flake8](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/flake8.yml/badge.svg)](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/flake8.yml)
[![Pytest](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/pytest.yml/badge.svg)](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/pytest.yml)
[![Build+Test](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/build.yml/badge.svg)](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/build.yml)

# portuguese-pos-dict

This repository contains data and tools used to build dictionaries for Portuguese.

## Maintainer

The owner, maintainer, and main dev for this repository is @p-goulart. The shell and perl components may be better
explained by @jaumeortola, though.

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Dictionaries

Portuguese has **two** separate sets of dictionaries, with separate source data and scripts to handle them:

- **[speller dictionaries](data/spelling-dict/README.md)**: those used by the `MORFOLOGIK_RULE_PT_*` spelling rules for
  all Portuguese varieties;
- **[POS tagger dictionary](data/src-dict/README.md)**: those used by LT's part-of-speech tagger to add POS information
  to each word.

For more in-depth information about each type, check their respective READMEs.

## Structure

For Legacy Reasons™, this repository is structured as follows:
- for work with the **POS tagger dictionary**, use the bash and Perl scripts in [/pos_tagger_scripts](./pos_tagger_scripts/README.md);
- to build the **speller dictionary** and several other helper files that go in the LT repo, configure Poetry for this
  project and use the Python scripts in [/dict_tools](./dict_tools/README.md).

The folder [dict_tools](./dict_tools) is a Git submodule. In order for it to work as a Python package, you must define
it as a **sources root**. In PyCharm, you can do this by right-clicking the folder and selecting
`Mark Directory as > Sources Root`.

## Release

The release process is automated upon each new **tag** pushed to this repo.

As of January 2024, the release only goes as far as deploying the binaries to **staging** repositories on SonaType.

In order to actually release the new version, you must log in to SonaType, navigate to the staging repositories, select
the repository you'd like to deploy, and click `Release`. This does mean that, for now, only LT members with access
to LT's Sonatype account can actually release new versions.

Soon, this will be no longer be the case, and they will be released automatically whenever a new tag is pushed to
`main`. Since there are restrictions on who pushes to `main`, this should be safe.

### Versioning

These dictionaries use [semantic versioning](https://semver.org), as they are essentially libraries that can be
declared as dependencies by LT. We only use major and minor, without a patch number, e.g. `0.9`.

Note that, in order for LT to actually use the newly released version, you'll need to update the version of the
`portuguese-pos-dict` dependency in **LT**'s main `pom.xml` file.

### Outline

The release process involves a few steps:

- build a new POS tagger dictionary (see [here](./pos_tagger_scripts/README.md) to see how);
- build a new speller dictionary (see [here](./pt_dict/README.md) to see how);
- once all dictionaries are built, files in [/results/java-lt](./results/java-lt) will be updated;
- install them with Maven inside that directory:
  ```bash
  mvn clean install
  ```
- and now, in the same directory, release them with:
  ```bash
  mvn clean deploy -P release
  # doing this without setting up SonaType and GPG secrets may prompt you for credentials multiple times!
  # make sure you are using 1password to handle secrets efficiently and securely ;)
  ```
- once this is done, you must log in to [SonaType](http://oss.sonatype.org/), navigate to the
  [Staging Repositories](https://oss.sonatype.org/#stagingRepositories), select the repository you'd like to deploy,
  and click `Release`.

Parts of this process will probably be automated as a part of a GitHub Actions workflow soon (as of November 2023, this
has not yet been done).

Note that, as per the instructions [here](#versioning), in order for your changes to be actually used by LT, you must
first have updated all `pom.xml` versions.


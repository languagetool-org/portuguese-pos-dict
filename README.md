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
declared as dependencies by LT.

As of May 2024 (with release `v1.0.0`), we are using the following versioning scheme:
- update the **major** (i.e. the first number) for *breaking* changes;
    - these are changes that depend on **code** changes in LT, e.g.:
      - changes to the way dictionaries built or loaded;
      - changes to the logic of Portuguese word tokenisation, POS tagging, or spellchecking;
      - changes that would necessitate **extensive** rewriting of the Portuguese XML rules.
- update the **minor** (i.e. the second number) for *new features*;
    - primarily, this will mean new words added to either the spelling or the tagging dictionary;
- update the **patch** (i.e. the third number) for *bug fixes*;
    - this includes typos, incorrect POS tags, or any other minor errors in the dictionaries that do not constitute
      'new content'.

Note that, in order for LT to actually use the newly released version, you'll need to update the version of the
`portuguese-pos-dict` dependency in **LT**'s main `pom.xml` file.

### Recommended workflow

If you are not a maintainer but you want to contribute words to the dictionaries,
it should be relatively simple. There are many steps, but they are all quite straightforward:

1. in the main [LanguageTool repo](https://github.com/languagetool-org/languagetool), branch out from `master`
   and push it (even if it doesn't have any changes yet);
   - if you know what you are doing, and your changes are a bit more complex, you may want to add
     some custom tests to the `MorfologikPortugueseSpellerRuleTest` class;

2. copy the branch name and add that to the `LT_BRANCH` variable in the [build.yml](.github/workflows/build.yml)
   workflow file in this repo:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11"]
    env:
      LT_BRANCH: "pt/dict/v015" ## <- here, set this to the branch you created
```

3. branch out of `main` in this repo, and make your changes;

4. commit and push your changes, and create a pull request;

5. the test workflow will run, testing your changes against the LT branch you specified;

6. if the tests pass and the PR is approved, merge it;

7. create a new tag for the merged commit, and push it to the repo (the tag will be
   the new dictionary version, so make sure it adhered to our versioning scheme!);

8. the release workflow will run, deploying the new version to Sonatype;

9. log in to Sonatype and release the new version (this part might be automated away in the future);

10. wait 10-20 minutes — it takes a while for the new version to be propagated,
    so it may not be immediately available to LT;

11. update the `portuguese-pos-dict` dependency in LT's `pom.xml` file to the new version;

12. push the changes to LT's repo, and wait for the CI to run all the tests;

13. if everything is green, merge the changes to `main` in LT's repo; the new version of the dictionaries
    should now be available to all LT users!

[![Flake8](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/flake8.yml/badge.svg)](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/flake8.yml)
[![Pytest](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/pytest.yml/badge.svg)](https://github.com/languagetool-org/portuguese-pos-dict/actions/workflows/pytest.yml)

# portuguese-pos-dict

This repository contains data and tools used to build dictionaries for Portuguese.

## Maintainer

The owner, maintainer, and main dev for this repository is @p-goulart. The shell and perl components may be better
explained by @jaumeortola, though.

## Dictionaries

Portuguese has **two** separate sets of dictionaries, with separate source data and scripts to handle them:

- **[speller dictionaries](data/spelling-dict/README.md)**: those used by the `MORFOLOGIK_RULE_PT_*` spelling rules for
  all Portuguese varieties;
- **[POS tagger dictionary](data/src-dict/README.md)**: those used by LT's part-of-speech tagger to add POS information
  to each word.

For more in-depth information about each type, check their respective READMEs.

## Scripts

This repository contains two independent sets of scripts:
- for work with the **POS tagger dictionary**, use the bash and Perl scripts in [/pos_tagger_scripts](./pos_tagger_scripts/README.md);
- to build the **speller dictionary** and several other helper files that go in the LT repo, configure Poetry for this
  project and use the Python scripts in [/pt_dict](./pt_dict/README.md).

## Release

### Dependencies

In order to release the dictionaries, you will need all dependencies listed for each set of scripts:
- [here](./pos_tagger_scripts/README.md#requirements) are the requirements for the POS tagger dictionary;
- and [here](./pt_dict/README.md#setup) are the dependencies for the speller.

In addition to those, you will also need:
- [Maven](https://maven.apache.org/install.html), to compile, install, and release the Java components;
- some way of managing [GPG](https://www.gnupg.org/download/) keys;
  - and, well, you will need to have your own key [generated](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)
    and [published](https://askubuntu.com/questions/220063/how-do-i-publish-a-gpg-key) to one or more key servers.

### Necessary credentials

In addition to being capable of GPG-signing your Maven deployments, you will also need the LT credentials to
[SonaType](http://oss.sonatype.org/), so you can deploy the binaries.

If you are an LT team member, you should have access to these credentials in a shared 1password vault (their name there
is `SonaType`). If you are an opensource developer (i.e. not an LT employee or freelance collaborator) and would still
like to release your own version of the dictionary, please contact the [maintainers](#maintainer).

#### GPG setup

The [pom.xml](./results/java-lt/pom.xml) file in thsi repo is set up to take GPG credentials from your environment:

```xml
    <!-- ... -->
    <properties>
        <!-- ... -->
        <gpg.keyname>${env.GPG_KEYNAME}</gpg.keyname>
        <gpg.passphrase>${env.GPG_PASSPHRASE}</gpg.passphrase>
    </properties>
    <!-- ... -->
```

But, of course, do **not** store your GPG credentials in plaintext. If you have the 1password CLI set up, make sure you
handle your secrets with 1password and call the release command with `op run --`, like:

```bash
op run -- mvn clean deploy -P release
```

### Versioning

These dictionaries use [semantic versioning](https://semver.org), as they are essentially libraries that can be
declared as dependencies by LT.

The version of a **new** release of the dictionary must be updated in **two** places for LT to actually use your
changes:
- in **this** repository, the [pom.xml](./results/java-lt/pom.xml) file must have `<version>` incremented
  (⛔️ **not** `<modelVersion>` ⛔️);
- in the `languagetool` project, the main `pom.xml` must have the Portuguese POS dict version updated;
- the specific value to be updated is that of `<portuguese-pos-dict.version>`.

To make things a little easier, in this repository you won't need to update the version in the `pom.xml` file yourself.
The XML contains the following environment variable:

```xml
<version>${env.PT_DICT_VERSION}</version>
```

You can call `mvn` with the specific version you want to release like so:
```bash
PT_DICT_VERSION="foo" mvn clean install
```

Or you can set up your environment to smartly get the version from the latest tag in this repository. In your bash or
zsh configuration file, add something like this:

```bash
export PT_DICT_HOME="${LT_ROOT}/portuguese-pos-dict"
dict_version() {
  git --work-tree "${PT_DICT_HOME}" describe --tags --abbrev=0 | sed 's/^v//g'
}
export PT_DICT_VERSION=$(dict_version)
```

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


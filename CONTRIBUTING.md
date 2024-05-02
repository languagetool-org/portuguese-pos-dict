# Contributing

We welcome contributions from the community and are happy to have them! It was the OS community that has made the
LT Portuguese project so successful, and we are committed to making it as easy as possible for new contributors.

That being said, the situation with the Portuguese dictionaries is quite complex, and we have a few guidelines that we
need contributors to follow. This is to ensure that the project is maintainable and that it grows in a sustainable way.

## Getting Started

The `main` branch is the default branch, and it is **protected**. Only admins are able to (but not encouraged!) to push
directly to it. All changes should be proposed via pull requests.

## Reviews

All submissions, including submissions by project members, require review. For now, please prefer @p-goulart or
@susanaboatto as your reviewers.

## Automated Checks

We have a few automated checks in place. The most important one, if you are making changes to the source dictionary
data, is the `Build` check. This workflow will **build** the binary dictionaries from your modified data and then
run standard LT tests. If the tests fail, the build will fail, and you will need to fix the issue before your PR can be
merged.

Note that the `Build` check can take a while to run, so please be patient. This is because we need to compile Hunspell
from source, compile LT from source, build the tagger dictionary... and then recompile LT with the new tagger logic,
which is used by the spelling dictionary compilation scripts... And then, on top of that, run the LT tests, which can
be quite time-consuming. With no caching, this can take up to ca. 17 minutes.

We have a separate workflow specifically designed simply to check if all status are passing. Because of how long it
takes to run the `Build` check, this workflow may sometimes fail because of a timeout. If that happens, you can simply
re-trigger it once all statuses are passing and your PR will be good to go.

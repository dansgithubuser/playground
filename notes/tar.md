`tar` has a lot of history and write-friendliness. Let's review readable versions of invocations, and tie them to their shortforms.

Each long-form option has a short-form option. Args can generally migrate to the end of the invocation, with the archive coming first and contents of the archive after. Short-form options can be grouped as usual, and if we keep them at the start we can also drop the initial dash.

## create a compressed archive
`tar --create --auto-compress --file=archive.tbz2 file1 file2 folder1 folder2`

There's some ambiguity around where args go. For whatever reason, `--create` takes no arg but expects a list of inputs at the end. `--file` seems to always refer to the archive.

shortform: `tar caf archive.tbz2 file1 file2 folder1 folder2`

## list contents of an archive
`tar --list --verbose --file=archive.tbz2`

shortform: `tar tvf archive.tbz2`

We can list a specific folder afterward:
`tar --list --verbose --file=archive.tbz2 folder1`

## extract contents of an archive
`tar --extract --verbose --file=archive.tbz2`

shortform: `tar xvf archive.tbz2`

We can be a little more specific:
`tar --extract --wildcards --verbose --file=lol.tbz2 'folder1/*.log'`

We need the `--wildcards` option to use `*`. `--wildcards` has no shortform.

We can use `--directory=/some/other/path` to extract to a different path. `-C` is the shortform for `--directory`.

## file name transformations
So far, we're missing a pretty practical option that hits on a subtle problem. We'd often like to extract a subset of an archive into a destination folder, but so far the structure inside the archive must always be preserved. It's not easy to explain what we'd like to do. `tar` gives us one option for typical use, and an explicit verbose one.

This will put the contents of `folder1` into `/some/other/path`:
`tar --extract --verbose --file=archive.tbz2 --directory=/some/other/path --strip-components=1 folder1`

We can use `--transform` option instead to specify a `sed` replace expression.

Neither of these options have shortforms.

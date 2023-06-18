# Usage

To apply the filter, use the following option with pandoc:

~~~shell
$ pandoc --filter pandoc-beamer-block
~~~

## Explanation

In the metadata block, specific set of classes can be defined to
decorate `div` elements by blocks

The metadata block add information using the `pandoc-beamer-block` entry
by a list of definitions:

``` yaml
pandoc-beamer-block:
  - classes: [info]
  - classes: [alert]
    type: alert
```

The metadata block above is used to add a `block` environment around
`div`s which have `info` class and a `alertblock` environment to `div`s
that have only a `alert` class.

Each entry of `pandoc-beamer-block` is a YAML dictionary containing:

- `classes`: the set of classes of the `div`s to which the
  transformation will be applied. This parameter is mandatory.
- `type`: the block type (either `alert`, `example` or `info`)

## Example

Demonstration: Using
[pandoc-beamer-block-sample.txt](https://raw.githubusercontent.com/chdemko/pandoc-beamer-block/develop/docs/images/pandoc-beamer-block-sample.txt)
as input gives output file in
[pandoc-beamer-block-sample.pdf](https://raw.githubusercontent.com/chdemko/pandoc-beamer-block/develop/docs/images/pandoc-beamer-block-sample.pdf).

``` console
$ pandoc \
    -t beamer \
    -V theme:Warsaw \
    --filter pandoc-beamer-block \
    -o docs/images/pandoc-beamer-block-sample.pdf \
    docs/images/pandoc-beamer-block-sample.txt
```

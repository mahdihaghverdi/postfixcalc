- `v0.8.1`
  - bump to version `v0.8.1`
  - make `stranswer` a regular method, and add a slicing behaviour to it and test it;
  - transfer `Calc` to calcobject.py module;

- `v0.8.0`
  - bump to version `v0.8.0`
  - add str_repr_timeout to `Calc` type

- `v0.7.2`
 - bump to version `v0.7.2`
 - fix error message of str repr

- `v.0.7.1`
  - bump to version `v0.7.1`
  - fix integer str conversion

- `v0.7.0`
  - bump to version `v0.7.0`
  - Implement `stranswer` property and test it

- `v0.6.0`
  - bump to version `v0.6.0`
  - Make the calculations safe with multiprocessing => put a timeout on processing the `answer`

- `v0.5.0`
  - Bump to version `v0.5.0`
  - Fix the bug for one digit input and complete the README.md
  - Write `Calc` type and change how user should use this lib

- `v0.4.0`
  - Bump to version `v0.4.0`
  - make the `evaluate` api better and test it
  - write a brand-new parser with the help of python `ast` module
  - add README.md

- `v0.3.0`
  - Prepare package to be published to PyPI

- `v0.2.0`
  - upload source package
  - rename to be postfixcalc
  - rename plumacalc to postfixcalc
  - fix some bugs of infix_to_postfix
  - reimplement evaluate funcion and test it
  - reimplement infix_to_postfix and test it
  - refactor _inter to be `_make_num` and make it more flexible to translate `n.m` to float and test it
  - replace `**` with `^` of _black_format function and test it
  - remove `.n` parsing of _concat_dotted_numbers function
  - write black_format function and remove type hints
  - implement a function to concat dotted fraction numbers and test it

- `v0.1.0`
  - write down a simple evaluate function
  - initialize the parser of str math expressions
  - define main type aliases
  - Make plumacalc a package and refactor main.py to __main__.py
  - Initial Commit
  - Add online IDE url
  - Initial commit

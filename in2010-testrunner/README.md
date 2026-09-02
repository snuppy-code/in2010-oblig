IN2010 setup and testrunner

[Norsk versjon](./README.no.md)

### Installation

1. Download the lastest `in2010-testrunner.zip` from [releases](https://github.uio.no/IN2010/in2010-testrunner/releases) (don't use
the “download zip” under the clone menu).
2. Either:
   - Run the program directly using `python path/to/file.zip`, or
   - install it using `pip install path/to/file.zip`.

> Note:
> On some operating systems it can be problematic to install
> python packages globally with `pip`. You can then either run the file
> directly without installing it, or [create a virtual python environment](https://docs.python.org/3/library/venv.html).

### Usage

1. Start by creating an empty directory to store your code in.
2. If you haven’t installed with `pip`, move `in2010-testrunner.zip` to the new directory
3. From within the newly created directory, run `in2010-testrunner` (or `python in2010-testrunner.zip`)
4. Write your solutions in the files created by `in2010-testrunner`.
5. Optionally delete source files you don’t need (`in2010-testrunner` creates both Java and Python source files)
6. Run your code with the `run` command in the `in2010-testrunner` prompt.
7. Make a zip file with the `zip` command in the `in2010-testrunner` prompt.
8. Upload the resulting zip file to [devilry](https://devilry.ifi.uio.no/devilry_student/)

### Development

> Note:
> These instructions are for developing the tool itself, and is not necessary
> for using the tool.

1. Create a python virtual environment. This can be done with `python -m venv .venv`
2. Activate the virtual environment `source .venv/bin/activate`
3. Install this package using `pip install -e .`. The `-e option` makes
   symlinks instead of copying the files, so you can edit them without
   reinstalling. If you add any new files you need ro rerun the command
4. make changes and run using `in2010-testrunner`

Step 1 and 2 can be automated using [direnv](https://direnv.net/) by adding `layout python` to `.envrc`

#!/usr/bin/env bash

set -e

# Ensure the resources are built properly
pushd test_resources > /dev/null
bash build.bash > /dev/null
popd > /dev/null

# Use the resources within test_resources
index="IN2010_OBLIG_INDEX=FILE://$(pwd)/test_resources/index.txt"
export "$index"

in2010_testrunner="python ../.."

# Cleanup the scratch dir, recreate it and enter it
rm -rf scratch
mkdir -p scratch
pushd scratch > /dev/null

printf "# Initial run of the tool\n\n"

echo "eksempelbruker" | $in2010_testrunner

# Disable the initial help message going forward for less cluttered logs
in2010_testrunner="$in2010_testrunner --disable-initial-help"

# In combination with dired, it makes debugging a bit easier. It should affect
# the tests whatsoever.
echo "export $index" > .envrc

# Run zip command

printf "\n\n# Run the zip command (expecting nothing but the command prompt)\n\n"
echo "zip" | $in2010_testrunner

# Check that the contents of the zip matches what we expect.
#
# Note:
#
#   The resulting zip is *not* identical to the current directory, so we check
#   that the source files match (as a heuristic).

printf "\n\n# Check the contents of the diff against the precode (expecting empty output)\n\n"

unzip_location=$(mktemp -d)
unzip *.zip -d "$unzip_location" > /dev/null
diff -r src/test_oblig "$unzip_location"/test_oblig || false

# Running testprograms

echo "Running testrunner"

# First run -- Not enough output

printf "\n# First run: expecting not enough output\n\n"

echo "run" | $in2010_testrunner

# Second run -- Fail

ln -sf fail.py src/test_oblig/task1.py
ln -sf Fail.java src/test_oblig/Task1.java

printf "\n\n# Second run: expecting fail\n\n"

echo "run" | $in2010_testrunner

# Third run -- Timeout

ln -sf timeout.py src/test_oblig/task1.py
ln -sf Timeout.java src/test_oblig/Task1.java

printf "\n\n# Third run: expecting timeout\n\n"

echo "run" | $in2010_testrunner

# Fourth run -- Pass

ln -sf pass.py src/test_oblig/task1.py
ln -sf Pass.java src/test_oblig/Task1.java

printf "\n\n# Fourth run: expecting pass\n\n"

echo "run" | $in2010_testrunner

popd > /dev/null

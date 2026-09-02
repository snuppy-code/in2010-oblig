from __future__ import annotations

import base64
import webbrowser
import configparser
import gettext
import hashlib
import io
import itertools
import json
import os
import pickle
import re
import subprocess
import sys
import tempfile
import typing as t
import zipfile
from argparse import ArgumentParser
from collections import OrderedDict
from contextlib import contextmanager
from dataclasses import dataclass
from functools import lru_cache
from modulefinder import ModuleFinder
from os.path import abspath, dirname, join, relpath
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from .class_file import ClassFile


def main():
    parser = ArgumentParser('in2010-testrunner')
    sub = parser.add_subparsers(dest='command', required=False)
    sub.add_parser("run")
    sub.add_parser("repl")
    sub.add_parser("update")
    sub.add_parser("zip")
    args = parser.parse_args()

    config = Config()
    cli = Cli()

    def load_or_die():
        try:
            config.load()
        except FileNotFoundError:
            cli.die("Not initialized. Are you sure you are "
                    "in the right directory")

    match args.command:
        case None | 'repl':
            # Read initial configuration
            try:
                config.load()
            except FileNotFoundError:
                init(config, cli)
                config.save()

            update(config)
            config.save()

            repl(config, cli)

        case 'update':
            load_or_die()
            update(config)
            config.save()
        case 'compile':
            load_or_die()
            compile_exercises(config.exercises)
        case 'zip':
            load_or_die()
            zip_files(config)

        case 'run':
            load_or_die()
            test_all_exercises(config.exercises, cli)


def repl(config: Config, cli: Cli):
    show_help(cli)

    while True:
        try:
            cmd = cli.input("cmd", sep="> ").split()
        except (KeyboardInterrupt, EOFError):
            break

        match cmd:
            case ("h" | "?" | 'help' | 'hjelp', *_):
                show_help(cli)

            case ('run' | 'kjør' | 'kjor' | 'r' | 'køyr', *_):
                test_all_exercises(config.exercises, cli)

            case ("update" | "oppdater", *_):
                update(config)
                config.save()

            case ('q' | 'quit' | 'avslutt', *_):
                return

            case ('clear' | 'cls', ):
                cli.clear()

            case ('kompiler' | 'compile' | 'c' | 'k', *_):
                compile_exercises(config.exercises)

            case ('reload', *_):
                config.load()

            case ('zip', *_):
                zip_files(config)

            case ('bug', *_):
                webbrowser.open("https://github.uio.no/IN2010/in2010-testrunner/issues/new")

            case _:
                cli.output("Command not found")


def show_help(cli: Cli) -> None:
    cli.output("Commands:")
    cli.output("    help, h     Print help")
    cli.output("    run         Run and test your code")
    cli.output("    update      Download new stuff")
    cli.output("    quit        Exit the program")
    cli.output("    clear       clear the screen")
    cli.output("    compile, c  Compile the java code")
    cli.output("    reload      Reload oppgaver.cfg")
    cli.output("    bug         Report a bug")
    cli.output("    zip         Make zip files")


def zip_files(config):
    for dir in Path("src").iterdir():
        with zipfile.ZipFile("oblig1.zip", "w") as zf:
            for path in dir.glob("**/*"):
                zf.write(path, relpath(path, "src"))
            oblig_cfg = configparser.ConfigParser()
            oblig_cfg['meta'] = config['meta']
            with zf.open("metadata", "w") as f:
                with io.TextIOWrapper(f) as f2:
                    oblig_cfg.write(f2)


def init(config: Config, cli: Cli):
    contents = set(x.name for x in Path(".").iterdir())
    if len(contents - {".git", ".vscode", ".idea", ".DS_Store", "in2010-testrunner.zip", "in2010-testrunner-main.zip"}):
        cli.die("This directory is not empty. Create and enter a new directory before using in2010-testrunner")

    cli.output("If you’re a group with more than one person, "
               "write all usernames with spaces between")
    config.add_section('meta')
    config['meta']['username'] = cli.input("UiO username")


def update(config: configparser.ConfigParser):
    defaut_index = ("https://www.uio.no/studier/emner/matnat/ifi/"
                    "IN2010/h26/innleveringer/filer/index.txt")
    index = os.environ.get("IN2010_OBLIG_INDEX", defaut_index)
    with urlopen(index) as res:
        urls = [urljoin(index, line.decode("utf-8")) for line in res]

    if os.path.exists("downloaded.json"):
        with open("downloaded.json") as f:
            downloaded = set(json.load(f))
    else:
        downloaded = set()

    for url in urls:
        if url in downloaded:
            continue
        with tempfile.TemporaryFile(mode="w+b") as f:
            with urlopen(url) as res:
                f.write(res.read())
            f.seek(0)
            install_zipfile(config, f)
        downloaded.add(url)

    with open("downloaded.json", "w") as f:
        json.dump(list(downloaded), f)


def install_zipfile(config: configparser.ConfigParser, file):
    with zipfile.ZipFile(file, "r") as zf:
        for member in zf.filelist:
            if member.filename == "oppgaver.cfg":
                with zf.open(member) as f2:
                    content = f2.read().decode("utf-8")
                    config.read_string(content)
            elif not os.path.exists(member.filename):
                zf.extract(member)


def test_all_exercises(exercises: list[Exercise], cli: Cli):
    file_hasher = FileHasher()
    java_exercises = compile_exercises(exercises)
    classes = ClassFileCache()

    for exercise in exercises:
        if exercise.python_main is not None and (Path("src") / exercise.python_main).exists():
            result_python = test_exercise(
                exercise, file_hasher, 'python',
                [sys.executable,
                 join("src", exercise.python_main)],
                lambda: python_source_files(exercise))
            print_test_result(cli, exercise, 'python', result_python)

        if exercise in java_exercises:
            if exercise.java_main is None and (class_source_path(exercise.java_main)).exists():
                continue
            result_java = test_exercise(
                exercise, file_hasher, 'java',
                ['java', '-cp', 'out', exercise.java_main],
                lambda: classes.class_closure(exercise.java_main).keys())
            print_test_result(cli, exercise, 'java', result_java)


def print_test_result(cli: Cli, exercise: Exercise, language: str,
                      result: None | tuple[str, TestFail]):
    match result:
        case None:
            cli.output("{exercise} - {language} - OK",
                       exercise=exercise.title,
                       language=language)
        case case, TimelimitExceeded(timeout_seconds=seconds):
            cli.output(
                "{exercise} - {language} - {case}: used more than {seconds}s",
                exercise=exercise.title,
                language=language,
                case=case,
                seconds=seconds)

        case case, VerificationFailed(message=message):
            cli.output(
                "{exercise} - {language} - {case}: wrong output: ‘{message}’",
                exercise=exercise.title,
                language=language,
                case=case,
                message=message)

        case case, WrongOutput(expected=None, linenum=linenum):
            cli.output(
                "{exercise} - {language} - {case}: too much output. "
                "line {linenum} should not exist",
                exercise=exercise.title,
                language=language,
                case=case,
                linenum=linenum)

        case case, WrongOutput(got=None, linenum=linenum):
            cli.output("{exercise} - {language} - {case}: not enough output",
                       exercise=exercise.title,
                       language=language,
                       case=case,
                       linenum=linenum)

        case case, WrongOutput(expected=expected, got=got, linenum=linenum):
            cli.output(
                "{exercise} - {language} - {case}: wrong output at "
                "line {linenum}. Expected ‘{expected}’, got ‘{got}’",
                exercise=exercise.title,
                language=language,
                case=case,
                linenum=linenum,
                expected=expected,
                got=got)

        case case, ProgramCrashed(error_message=error_message):
            cli.output(
                "{exercise} - {language} - {case}: "
                "crashed with error message:",
                exercise=exercise.title,
                language=language,
                case=case)
            print(error_message)


def test_exercise(
    exercise: Exercise,
    file_hasher: FileHasher,
    language: str,
    command: list[str | Path],
    find_hash_files: t.Callable[[], t.Iterable[str]],
) -> None | tuple[str, TestFail]:

    assert exercise.java_main is not None

    # Figure out file paths
    key_file = f"out/{exercise.id}.{language}-test.key"
    result_file = f"out/{exercise.id}-{language}-result.pickle"

    # Save already computed result
    if file_hasher.check_key(key_file):
        with open(result_file, "rb") as f:
            return pickle.load(f)

    # Actually run the tests
    error: tuple[str, TestFail] | None = None
    for test_case in find_tests(Path(exercise.tests_dir)):
        output_path = Path(
            "out") / f"{exercise.id}-{test_case.id}-java-output.txt"
        e = run_test(command, test_case, output_path)
        if e is not None:
            error = (test_case.id, e)
            break

    # Save the result and create key
    with open(result_file, "wb") as f:
        pickle.dump(error, f)
    file_hasher.create_key(key_file, find_hash_files())

    return error


def run_test(command: list[str | Path], test_case: TestCase,
             actual_output: Path) -> None | TestFail:
    with (open_input(test_case.input) as stdin, open(actual_output, 'wb')
          as stdout):
        proc = subprocess.Popen(command,
                                stdin=stdin,
                                stdout=stdout,
                                stderr=subprocess.PIPE)

        timeout = False
        try:
            stderr = proc.stderr.read().decode('utf8')
            proc.wait(timeout=test_case.timeout_seconds)
        except subprocess.TimeoutExpired:
            timeout = True

        if timeout:
            return TimelimitExceeded(
                stderr_output=stderr,
                timeout_seconds=test_case.timeout_seconds)
        elif proc.returncode != 0:
            return ProgramCrashed(stderr)
        else:
            print(stderr, end="")
            return check_output(test_case.correct_output, actual_output)


@contextmanager
def open_input(path: Path):
    if path.name.endswith(".py"):
        proc = subprocess.Popen([sys.executable, path])
        yield proc.stdout
    else:
        with open(path, "rb") as file:
            yield file


def check_output(correct_output: Path, actual_output: Path) -> TestFail | None:
    with open(actual_output) as actual_output_file:
        if correct_output.name.endswith(".py"):
            result = subprocess.run([sys.executable, correct_output],
                                    stdin=actual_output_file,
                                    stdout=subprocess.PIPE)

            if len(result.stdout) != 0:
                return VerificationFailed(result.stdout.decode("utf8"))
            else:
                return None
        else:
            with open(correct_output) as correct_output_file:
                # Compare line by line in case there is different
                # types of newlines
                for line, (correct, actual) in enumerate(itertools.zip_longest(
                        correct_output_file,
                        actual_output_file)):
                    correct = correct and correct.rstrip("\r\n")
                    actual = actual and actual.rstrip("\r\n")
                    if correct != actual:
                        return WrongOutput(line, correct, actual)

    return None


@lru_cache()
def find_tests(directory: Path) -> list[TestCase]:
    test_config = configparser.ConfigParser()
    if (fn := directory / "tests.cfg").exists():
        with open(fn) as f:
            test_config.read_file(f)

    input_files = dict[str, Path]()
    output_files = dict[str, Path]()

    exp = re.compile(r"(.*)\.(input|output).(?:txt|py)")
    for file in directory.iterdir():
        if (m := exp.fullmatch(file.name)) is not None:
            name = m.group(1)
            if m.group(2) == 'input':
                input_files[name] = file
            else:
                output_files[name] = file

    test_cases = list[TestCase]()

    test_ids = set(input_files.keys()).intersection(output_files.keys())
    for case in sorted(test_ids):
        if case not in test_config:
            test_config.add_section(case)
        timeout_seconds = test_config.get(  #
            case, "timeout-seconds", fallback="1")

        test_cases.append(
            TestCase(case,
                     input_files[case],
                     output_files[case],
                     timeout_seconds=int(timeout_seconds)))

    return test_cases


def compile_exercises(exercises: list[Exercise]) -> list[Exercise]:
    os.makedirs("out", exist_ok=True)

    # step 1: Figur out what to compile
    exercises = [
        exercise  #
        for exercise in exercises  #
        if exercise.java_main is not None
        and class_source_path(exercise.java_main).exists()
    ]
    exercises_to_compile = find_changed(exercises, "java-compile")
    if len(exercises_to_compile) == 0:
        return exercises  # Great! Nothing to compile

    # step 2: Run javac to actually compile
    java_files = [
        class_source_path(e.java_main)  #
        for e in exercises if e.java_main is not None
    ]
    run_javac(*java_files, source_dir=Path("src"), destdir=Path("out"))
    file_hasher = FileHasher()  # Create new file hasher to clear cache

    # step 3: Creath key files containing hash values to
    # remove the files in step 1 if we rerun without
    # changing them
    class_file_cache = ClassFileCache()
    for exercise in exercises_to_compile:
        classes = class_file_cache.class_closure(exercise.java_main)
        java_files = list({
            Path("src") / relpath(dirname(f), "out") / cls.source_file
            for f, cls in classes.items()
        })
        keyfile = f"out/{exercise.id}.java-compile.key"
        file_hasher.create_key(keyfile, java_files)

    return exercises


def find_changed(exercises: list[Exercise], key: str) -> list[Exercise]:
    file_hasher = FileHasher()
    return [
        exercise for exercise in exercises
        if not file_hasher.check_key(f"out/{exercise.id}.{key}.key")
    ]


class ClassFileCache:

    def __init__(self) -> None:
        self.cache: dict[str, ClassFile] = {}

    def load(self, path: str | Path) -> ClassFile:
        path = str(path)  # normalize
        if path in self.cache:
            return self.cache[path]
        with open(path, "rb") as file:
            classfile = ClassFile(file)
        self.cache[path] = classfile
        return classfile

    def class_closure(self, start_class_name):
        """Find all dependencies of class using DFS"""

        start_class_file = class_file_path(start_class_name)
        start_class = self.load(start_class_file)

        # our visited set
        class_files = {start_class_file: start_class}

        # worklist of not yet visited classes
        stack = [start_class]

        while stack:
            current_class = stack.pop()

            for neighbor_class_name in current_class.class_names:
                neighbor_class_file = class_file_path(neighbor_class_name)
                if not neighbor_class_file.exists():
                    # builtin class or something.
                    # We don't care about it
                    continue

                neighbor_class = self.load(neighbor_class_file)
                if neighbor_class_file not in class_files:
                    class_files[neighbor_class_file] = neighbor_class
                    stack.append(neighbor_class)
        return class_files


class FileHasher:

    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def create_key(self, path, files):
        """Create file with hash of files at path

        Create file storing the hash values `files` and store
        it at path. The function `check_key` can later be
        called with the same `path` to check if any of the
        files have changed.
        """

        hashes = {}
        for file in files:
            hash_value = self.hash_file(file)
            hashes[relpath(file, dirname(path))] = hash_value

        with open(path, "wb") as file:
            pickle.dump(hashes, file)

    def check_key(self, path: Path | str) -> bool:
        """See create_key

        Returns True when nothing has changed
        """
        try:
            with open(path, 'rb') as file:
                hashes = pickle.load(file)
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            os.remove(path)
            return False

        for file_name, file_hash in hashes.items():
            file_name = join(dirname(path), file_name)
            if not self.check_file(file_name, file_hash):
                os.remove(path)
                return False

        return True

    def check_file(self, path, expected) -> bool:
        """Return true if file at path exists and is not changed"""
        try:
            return self.hash_file(path) == expected
        except FileNotFoundError:
            return False

    def hash_file(self, path) -> str:
        if path not in self.cache:
            with open(path, "rb") as file:
                value = hashlib.sha512(file.read()).digest()
            self.cache[path] = base64.encodebytes(value).decode("ascii")
        return self.cache[path]


def python_source_files(exercise: Exercise) -> set[str]:
    """Figure out which source files an exercise depends on"""
    if exercise.python_main is None:
        return set()
    source_file = join(abspath("src"), exercise.python_main)
    source_dir = dirname(source_file)
    finder = ModuleFinder(path=[source_dir])
    finder.run_script(source_file)
    return {
        module.__file__
        for module in finder.modules.values()  #
        if hasattr(module, '__file__') and module.__file__ is not None
        and abspath(module.__file__).startswith(source_dir)
    }


def class_file_path(class_: str) -> Path:
    """Convert fully qualified class name to file path"""
    return Path('out') / (class_.replace('.', '/') + '.class')


def class_source_path(class_: str) -> Path:
    """Convert fully qualified class name to file path

    Unlike `class_file_path`, this assumes that the java
    code follows some conventions. Specifically tha convention
    that java classes are located in file named ClassName.java
    where ClassName is the name of the class
    """
    return Path('src') / (class_.replace('.', '/') + '.java')


def run_javac(*files,
              source_dir: str | Path | None = None,
              destdir: str | Path | None = None):
    args: list[str | Path] = ['javac', '-encoding', 'UTF-8']
    if source_dir is not None:
        args.extend(["--source-path", source_dir])
    if destdir is not None:
        args.extend(["-d", destdir])
    args.extend(files)
    subprocess.run(args=args)


@dataclass
class Exercise:
    id: str  # Used in file names and stuff
    title: str  # Displayed to the user
    python_main: str | None  # ralative path from 'src'
    java_main: str | None  # fully qualified class name
    tests_dir: str


@dataclass
class TestCase:
    id: str
    input: Path
    correct_output: Path
    timeout_seconds: int


class Config(configparser.ConfigParser):
    path = "oppgaver.cfg"

    def __init__(self):
        super().__init__(dict_type=OrderedDict)

    def load(self):
        with open(self.path, "r") as file:
            self.read_file(file)

    def save(self):
        with open(self.path, "w") as file:
            self.write(file)

    @property
    def exercises(self) -> list[Exercise]:
        result: list[Exercise] = []
        for section_name, section in self.items():
            if not section_name.startswith('oppgave.'):
                continue

            id = section_name.removeprefix('oppgave.')

            exercise = Exercise(
                id=id,
                title=section.get('title', id),
                python_main=section.get('python-main'),
                java_main=section.get('java-main'),
                tests_dir=section.get('test-dir', f'testfiles/{id}'),
            )
            result.append(exercise)
        return result


class Cli:

    def __init__(self):
        localedir = Path(__file__).parent / "i18n"
        gettext.bindtextdomain("messages", localedir)
        gettext.textdomain("messages")

        try:
            import prompt_toolkit
            self.session = prompt_toolkit.PromptSession()
        except ImportError:
            self.session = None

    def input(self, format: str, *args, sep=": ", **kwargs) -> str:
        format = gettext.gettext(format)
        prompt = format.format(*args, **kwargs) + sep
        if self.session:
            return self.session.prompt(prompt)
        else:
            return input(prompt)

    def output(self, format: str, *args, **kwargs) -> None:
        format = gettext.gettext(format)
        print(format.format(*args, **kwargs))

    def clear(self) -> None:
        print(end="\x1b[2J\x1b[H")

    def die(self, format: str, *args, code=1, **kwargs) -> None:
        self.output(format, *args, **kwargs)
        sys.exit(code)


def first_truthy(iter, pred=lambda x: x):
    for x in iter:
        if pred(x):
            return x


class TestFail:
    pass


@dataclass
class TimelimitExceeded(TestFail):
    stderr_output: str
    timeout_seconds: int


@dataclass
class ProgramCrashed(TestFail):
    error_message: str


@dataclass
class WrongOutput(TestFail):
    linenum: int
    expected: str | None
    got: str | None


@dataclass
class VerificationFailed(TestFail):
    message: str

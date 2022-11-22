import subprocess
import argparse
from pathlib import Path
import re
from multiprocessing import Pool
from sty import fg, ef
import locale
import os
import sys

# Get locale
_, LOC = locale.getlocale()

# Init colors
BOLD  = ef.bold
ITAL  = ef.italic
RESET = fg.rs + ef.rs

RED    = fg.red
GREEN  = fg.green
GRAY   = fg.da_grey
YELLOW = fg.yellow

# Init class regex
CLASS_REGEX = r"class (\S+)\((Scene|ThreeDScene|Slide|ThreeDSlide)\):"

# Number of threads for rendering
N_THREADS = 5

# Path to log folder
LOG_PATH = Path("logs")

# Create log folder if it does not exist
if not LOG_PATH.is_dir():
    os.mkdir(str(LOG_PATH))


def findAllClasses(f):
    """
        A function that searches the file f for 
        renderable classes and returns them in an array
    """

    out = []
    l = f.readline()

    while l:
        # Go over lines in f and find class names
        class_name = re.findall(CLASS_REGEX, l)

        if class_name:
            out.append(class_name[0][0])
        l = f.readline()

    return out

def findClassByLine(f, line):
    """
        A function that finds which class contains
        the given line number
    """

    last_class = ""
    line_count = 1
    l = f.readline()
    
    while l and line_count <= line:
        # Go over lines in f and keep track of last spotted class
        # until we hit the given line

        class_name = re.findall(CLASS_REGEX, l)

        if class_name:
            last_class = class_name[0][0]

        line_count += 1
        l = f.readline()

    return last_class

def renderScene(scene, args="qp"):
    """
        A function that renders the given scene with the
        provided args
    """

    # Print some info and init command
    print(f"{YELLOW + BOLD}STARTING{RESET} - {scene}")

    command = [
        "manim",
        file_path,
        scene,
        f"-{args}",
    ]

    # Start render
    res = subprocess.Popen(
        command, 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    _, error_log = res.communicate()

    # Get log path
    logpath = LOG_PATH / f"{scene}.log"

    # We got an error
    if res.returncode != 0:
        print(f"{RED + BOLD}ERROR   {RESET} - {scene}")

        with open(logpath, "wb") as f:
            # Write log file
            f.write(error_log.decode(LOC).encode("utf-8"))

    else:
        # Everything ok so we can remove the last error log from this scene
        if logpath.exists():
            print(f"{GRAY + ITAL}Removing log {logpath}{RESET}")
            logpath.unlink()

        print(f"{GREEN + BOLD}FINISHED{RESET} - {scene}")


# Init argparser
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--line', type=int)
parser.add_argument('-m', '--manim_args')
parser.add_argument('-c', '--class_name')
parser.add_argument('-l', '--list_classes', action='store_true')

args = parser.parse_args()

file_path = Path(args.filename)

if __name__ == "__main__":
    # Check if file is valid
    if file_path.is_file():
        with open(file_path) as f:

            # We got a class name
            if args.class_name:
                cname = args.class_name

                # Check if class name valid
                if cname not in findAllClasses(f):
                    print(f"No class found with name '{cname}'")
                    sys.exit(1)

            # We got a line number
            elif args.line is not None:
                cname = findClassByLine(f, args.line)

                if not cname:
                    print(f"No class at line number {args.line}")
                    sys.exit(1)
            
            # We are listing classes
            elif args.list_classes:
                print(*findAllClasses(f), sep="\n")
                sys.exit(0)

            # Render all
            else:
                classes = findAllClasses(f)
                pool = Pool(5)

                with pool:
                    pool.map(renderScene, classes)

                sys.exit(0)

        # Process args
        manim_args = f"-{args.manim_args}" if args.manim_args else ""

        # Init command
        command = [
            "manim",
            file_path,
            manim_args,
            cname
        ]

        # Run render
        subprocess.run(command)


    else:
        print(f"Could not open file {file_path}")
        sys.exit(1)

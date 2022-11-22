import subprocess
import argparse
from pathlib import Path
import re
from multiprocessing import Pool
from sty import fg, ef
import locale
import os

_, LOC = locale.getlocale()

BOLD  = ef.bold
ITAL  = ef.italic
RESET = fg.rs + ef.rs

RED    = fg.red
GREEN  = fg.green
GRAY   = fg.da_grey
YELLOW = fg.yellow


CLASS_REGEX = r"class (\S+)\((Scene|ThreeDScene|Slide|ThreeDSlide)\):"
N_THREADS = 5

LOG_PATH = Path("logs")

if not LOG_PATH.is_dir():
    os.mkdir(str(LOG_PATH))

def findAllClasses(f):
    out = []
    l = f.readline()

    while l:
        class_name = re.findall(CLASS_REGEX, l)

        if class_name:
            out.append(class_name[0][0])
        l = f.readline()

    return out

def findClassByLine(f, line):
    last_class = ""
    line_count = 1
    l = f.readline()

    while l and line_count <= line:
        class_name = re.findall(CLASS_REGEX, l)

        if class_name:
            last_class = class_name[0][0]

        line_count += 1
        l = f.readline()

    return last_class

def renderScene(scene, args="qp"):
    print(f"{YELLOW + BOLD}STARTING{RESET} - {scene}")
    command = [
        "manim",
        file_path,
        scene,
        f"-{args}",
    ]

    res = subprocess.Popen(
        command, 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    _, error_log = res.communicate()

    logpath = LOG_PATH / f"{scene}.log"

    if res.returncode != 0:
        print(f"{RED + BOLD}ERROR   {RESET} - {scene}")

        with open(logpath, "wb") as f:
            f.write(error_log.decode(LOC).encode("utf-8"))

    else:
        if logpath.exists():
            print(f"{GRAY + ITAL}Removing log {logpath}{RESET}")
            logpath.unlink()

        print(f"{GREEN + BOLD}FINISHED{RESET} - {scene}")



parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--line', type=int)
parser.add_argument('-m', '--manim_args')
parser.add_argument('-c', '--class_name')
parser.add_argument('-l', '--list_classes', action='store_true')

args = parser.parse_args()

file_path = Path(args.filename)

if args.line is None:
    args.line = 0


if __name__ == "__main__":
    if file_path.is_file():
        with open(file_path) as f:

            # We got a line number
            if args.line or args.class_name:

                # Get class name
                cname = args.class_name if args.class_name else findClassByLine(f, args.line)

                manim_args = f"-{args.manim_args}" if args.manim_args else ""

                if cname:
                    command = [
                        "manim",
                        file_path,
                        manim_args,
                        cname
                    ]

                    subprocess.run(command)

                else:
                    print("No class at that number!")

            elif args.list_classes:
                print(*findAllClasses(f), sep="\n")

            # Render all
            else:
                classes = findAllClasses(f)
                pool = Pool(5)

                with pool:
                    pool.map(renderScene, classes)



    else:
        print(f"Could not open file {file_path}")

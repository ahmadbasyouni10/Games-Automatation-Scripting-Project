# operating system module
# json for interpreting json files
# shutil copies and overwrites operations
# run any terminal command such as running go code
# command line arguments using sys

import os
import json
import shutil
from subprocess import PIPE, run
import sys

# keyword to find game paths in data
# used to search for file that has .go in games to compile
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


# function to find all game paths in given source dir
# only checks directories, returns directories with game in them
def find_all_game_paths(source):
    game_paths = []

    # walk will recursively look through all directories
    # we only need to run this one time for data
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths


# takes directory from each path and adds it to a new list with game not in the dir
def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names


def create_dir(path):
    # if directory doesn't exist make dir at path we pass
    if not os.path.exists(path):
        os.mkdir(path)


# takes the list with directories without _game and copies them into dest
# if dir already exists, we overwrite it
def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


# take the data we saved of game names and then number of games saved into json file (writing not reading)
def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return

    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)


def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result", result)

    # go back to original directory
    os.chdir(cwd)


# source is where we are looking
# target where we want to put new dir
def main(source, target):
    # current working dir where python file is ran
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    # takes paths we found from game_paths and add just the dir into a list without game included
    new_game_dirs = get_name_from_paths(game_paths, "_game")

    # creates the directory
    create_dir(target_path)

    # performs the copying by creating tuple from game_paths with the directory joins them
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)


# runs only when file is ran, helps import functions from this file without running
if __name__ == "__main__":
    # the args are source and target directory, ensures both passed
    # sys.argv is to access command line arguments
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only")

    # we don't want file name, so we start at index 1 for source and target
    source, target = args[1:]
    main(source, target)

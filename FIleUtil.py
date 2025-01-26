from LogPrint import print_uncolored, print_cyan, print_red


def get_line(file, string=False):
    try:
        with open(file, 'r') as file_:
            line = file_.read()
            if not string:
                line = float(line)
    except Exception as e:
        print_red("ERROR - FILE MANAGER",
                  f"The following exception was thrown during getting line from file = {file}: {type(e).__name__}")
        raise Exception
    print_cyan("FILE MANAGER",
               f"Get from {file} file, line = ",
               text_colored=f"\n{line}")
    return line


def update_file_value(file, new_value):
    try:
        with open(file, 'w') as file_:
            file_.write(new_value)
    except Exception as e:
        print_red("ERROR - FILE MANAGER",
                  f"The following exception was thrown during updating file ({file}) value: {type(e).__name__}, with value = {new_value}")
        raise Exception
    print_cyan("FILE MANAGER",
               f"Updated {file} file with value = ",
               text_colored=f"\n{new_value}")


def get_lines(file):
    try:
        with open(file, "r") as file_:
            lines = file_.readlines()
    except Exception as e:
        print_red("ERROR - FILE MANAGER",
                  f"The following exception was thrown during getting all lines from file = {file}: {type(e).__name__}")
        raise Exception
    print_cyan("FILE MANAGER",
               f"Get from {file} file lines = ",
               text_colored=f"\n{lines}")
    return lines


def add_line(file, value):
    try:
        with open(file, 'a') as file_:
            file_.write(value + "\n")
    except Exception as e:
        print_red("ERROR - FILE MANAGER",
                  f"The following exception was thrown during adding line to file = {file}: {type(e).__name__}, with value = {value}")
        raise Exception
    print_cyan("FILE MANAGER",
               f"Added to {file} file, line = ",
               text_colored=f"\n{value}")


def create_empty_file(file):
    try:
        with open(file, "w") as file_:
            pass
    except Exception as e:
        print_red("ERROR - FILE MANAGER",
                  f"The following exception was thrown during the creation of the empty file = {file}: {type(e).__name__}")
        raise Exception
    print_uncolored("FILE MANAGER",
                    f"Created the empty file = {file}")

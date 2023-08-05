import random


def split_include(input_string):
    try:
        result = input_string.split("#include")[1]
        try:
            return result.split("<")[1].split(">")[0]
        except:
            return result.split("\"")[1]

    except:
        return None


def write_list_to_file(include_list):
    with open("include_list", "a") as f:
        for item in include_list:
            f.write(" " + str(item))
        f.write("\n")


def text_editing():
    include_list = [""]
    counter = 0
    with open("outputC") as includes_linux:
        for includes in includes_linux:
            # print(includes)
            path_curr = includes.split(":")[0]
            include_curr = includes.split(":")[1]
            include_curr = split_include(include_curr)
            # print(include_curr)

            if (include_list[0] == path_curr):
                # kein wechsel
                counter = counter+1
                include_list.append(include_curr)

            else:
                include_list.append(counter+1)
                write_list_to_file(include_list)
                counter = 0
                include_list = [path_curr, include_curr]
                # liste schreiben, loeschen und path neu setzten


def main():
    text_editing()


if __name__ == "__main__":
    main()

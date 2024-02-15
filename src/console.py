# Python Console Module that allows to print BB code in terminal 
# Pimp your terminal with colors 
#  @toutjavascript  https://github.com/toutjavascript
#  V1 : 2024



import re
import inspect

# parse BB code and print it in console
def printBB(text):
    text=re.sub(r"(\[h1\])([^\[\]]+)(\[/h1\])", "\033[32;1m\\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[ok\])(.+)(\[/ok\])", "\033[32;1m\\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[error\])([^\[\]]+)(\[/error\])", "\033[31;1m\\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[b\])([^\[\]]+)(\[/b\])","\033[1m\\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[u\])([^\[\]]+)(\[/u\])","\033[4m\\2\033[24m",text,re.IGNORECASE)
    text=re.sub(r"(\[d\])([^\[\]]+)(\[/d\])","\033[2m\\2\033[22m",text,re.IGNORECASE)
    text=re.sub(r"(\[fade\])([^\[\]]+)(\[/fade\])","\033[2m\\2\033[22m",text,re.IGNORECASE)
    text=re.sub(r"(\[reset\])","\033[0m\033[49m",text,re.IGNORECASE)
    text=re.sub(r"(\[reverse\])(.+)(\[/reverse\])","\033[7m\\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[header\])([^\[\]]+)(\[/header\])","\\033[1m \\2\033[0m",text,re.IGNORECASE)
    text=re.sub(r"(\[hour\])([^\[\]]+)(\[/hour\])","\\033[48;5;255m\\2\033[0m",text,re.IGNORECASE)
    print(text)


def printExceptionError(error):
    caller_name = inspect.stack()[1].function
    file=inspect.stack()[1].filename
    file=file[file.rfind("\\")+1:]
    printBB("[error]Exception Error on [b]"+file+"/"+caller_name+"()[/b]: "+repr(error)+"[/error]")

# From this great tuto https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
def test():
    for i in range(30, 37 + 1):
        print("\033[%dm%d\t\t\033[%dm%d" % (i, i, i + 60, i + 60))

    print("\033[39m\\033[49m                 - Reset color")
    print("\\033[2K                          - Clear Line")
    print("\\033[<L>;<C>H or \\033[<L>;<C>f  - Put the cursor at line L and column C.")
    print("\\033[<N>A                        - Move the cursor up N lines")
    print("\\033[<N>B                        - Move the cursor down N lines")
    print("\\033[<N>C                        - Move the cursor forward N columns")
    print("\\033[<N>D                        - Move the cursor backward N columns\n")
    print("\\033[2J                          - Clear the screen, move to (0,0)")
    print("\\033[K                           - Erase to end of line")
    print("\\033[s                           - Save cursor position")
    print("\\033[u                           - Restore cursor position\n")
    print("\\033[4m                          - Underline on")
    print("\\033[24m                         - Underline off\n")
    print("\\033[1m                          - Bold on")
    print("\\033[21m                         - Bold off")
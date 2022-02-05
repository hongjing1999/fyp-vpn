import re

def del_user(user_list, delete_user):
    for i in user_list.split("\n"):
        if "  - " + delete_user == i:
            match = re.search(i, user_list)
            startIndex = match.start()
            endIndex = match.end()
            if(startIndex == 0):
                user_list = user_list[endIndex+1:]
            elif endIndex == len(user_list):
                user_list = user_list[:startIndex - 1] + user_list[endIndex:] + "\n"
            else:
                user_list = user_list[:startIndex - 1] + user_list[endIndex:]
            break
    if (not user_list.endswith("\n")):
        user_list = user_list + "\n"
    return user_list

# def del_user(user_list, delete_user):
#     user_list = user_list.replace("  - " + delete_user, "")
#     if(not user_list.endswith("\n")):
#         user_list = user_list + "\n"
#     return user_list

def add_user(user_list, new_user):
    for i in user_list.split("\n"):
        if "  - " + new_user == i:
           raise Exception("Drone exists")

    if(user_list.endswith("\n")):
        return user_list + "  - " + new_user + "\n"
    else:
        return user_list + "\n  - " + new_user + "\n"

def get_user_list():
    f = open("algo/config.cfg", "r")
    filetext = f.read()
    f.close()
    matchStart = re.search("users:", filetext)
    startIndex = matchStart.end()
    matchEnd = re.search("## end of user ##", filetext)
    endIndex = matchEnd.start()
    users = filetext[startIndex + 1:endIndex - 1]
    return users, filetext, startIndex, endIndex

def write_file(user_list, filetext, startIndex, endIndex):
    filetext = filetext[:startIndex + 1] + user_list + filetext[endIndex:]
    f = open("algo/config.cfg", "w")
    f.write(filetext)
    f.close()

# if __name__ == '__main__':
    # addUser: str = "test"
    # f = open("config.cfg", "r")
    # filetext = f.read()
    # f.close()
    # matchStart = re.search("users:", filetext)
    # startIndex = matchStart.end()
    # matchEnd = re.search("## end of user ##", filetext)
    # endIndex = matchEnd.start()
    # users = filetext[startIndex+1:endIndex-1]
    #
    # deletedList = del_user(users, "test")
    # addedList = add_user(deletedList, "dev")







import sys

from repositories.postgres import UserRepository

if __name__ == "__main__":
    try:
        username = sys.argv[1]
    except IndexError as ex:
        sys.exit("Username Not Provided")
    username = username.lower()
    if UserRepository.check_username_exist(username=username):
        UserRepository.make_admin(username=username)
    else:
        sys.exit("Provide a Valid Username")

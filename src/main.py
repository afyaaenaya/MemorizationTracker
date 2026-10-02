from quiz import start_quiz
from tracker import ProgressFileError

if __name__ == "__main__":
    try:
        start_quiz()
    except ProgressFileError as error:
        print(error)

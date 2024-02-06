from threading import Thread
from lesson import Lesson
from config import LOGGER

lessons = [
    ["8:30:0", "9:15:00", "7fder1h-S7hib9b67uPq3kRFd3XSY71GCjr-eB8asdk"],
]


def main():
    for lesson in lessons:
        l = Lesson(lesson[0], lesson[1], lesson[2])
        t = Thread(target=l.start)
        t.start()
        LOGGER.info(f"Processing lesson {lesson}")


if __name__ == "__main__":
    main()

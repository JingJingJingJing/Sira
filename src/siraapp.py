from fake_controller import SiraController
from model import SiraMode
from view import SiraApp


def main():
    view = SiraApp()
    model = SiraMode()
    controller = SiraController(view, model)
    view.set_controller(controller)
    view.run()


if __name__ == '__main__':
    main()

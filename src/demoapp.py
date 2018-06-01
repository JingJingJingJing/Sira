from controller import DemoController
from model import DemoMode
from view import DemoApp


def main():
    view = DemoApp()
    model = DemoMode()
    controller = DemoController(view, model)
    view.setController(controller)
    view.run()

if __name__ == '__main__':
    main()
from controller import SiraController
from view import SiraApp


def main():
    view = SiraApp()
    controller = SiraController(view)
    view.set_controller(controller)
    view.run()
    

if __name__ == '__main__':
    main()

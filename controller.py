from pyPS4Controller.controller import Controller

class MyController(Controller):
    def on_x_press(self):
        print("X pressed")

    def on_circle_press(self):
        print("Circle pressed")

    def on_triangle_press(self):
        print("Triangle pressed")

    def on_square_press(self):
        print("Square pressed")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
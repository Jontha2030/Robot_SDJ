from pyPS4Controller.controller import Controller

print("Starting controller...")

class MyController(Controller):
    def on_x_press(self):
        print("X pressed")

    def on_circle_press(self):
        print("Circle pressed")

    def on_triangle_press(self):
        print("Triangle pressed")

    def on_square_press(self):
        print("Square pressed")

controller = MyController(interface="/dev/input/event4", connecting_using_ds4drv=False)
print("Listening...")
controller.listen(timeout=60)
print("Stopped")
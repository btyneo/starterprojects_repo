import numpy as np
import tkinter as tk
from functools import reduce
from fractions import Fraction


class Calculator:
    def __init__(self):
        self.angle_mode = 'radians'
        self.rounded = 2
        self.stand_to_dec = True

    def add(self, *args):
        return reduce(lambda x, y: x + y, args)

    def subtract(self, *args):
        # the 'reduce' below basically takes first 2 elements from the 'args' and takes it as 'x' and 'y',
        # and then subtracts
        # so lambda takes

        return reduce(lambda x, y: x - y, args)

    def multiply(self, *args):
        return reduce(lambda x, y: x * y, args)

    def divide(self, *args):
        try:
            return reduce(lambda x, y: x / y, args)
        except ZeroDivisionError as error:
            print("\nError!\nCannot divide by 0\n")

    def squared(self, num):
        return num ** 2

    def cubed(self, num):
        return num ** 3

    def sqroot(self, num):
        if num >= 0:
            return num ** 0.5
        else:
            return 'Value must be greater than/equal to 0'

    def power(self, num, power):
        if power < 1 and num < 0:
            return "Value must be greater than/equal to 0"
        return num ** power

    def fraction_decimal_conversion(self, num):
        return Fraction(num).limit_denominator()

    def decimal_fraction_conversion(self, num):
        return float(num)

    def set_angle_mode(self, mode):
        if mode.lower() in ['radians', 'degrees']:
            self.angle_mode = mode.lower()
        else:
            raise ValueError("Invalid Angle. Try degrees or radians.")

    def round(self, num):
        return np.round(num, self.rounded)

    def sin(self, angle):
        # we need to convert angle to radians cuz thats what numpy expects
        if self.angle_mode == 'degrees':
            angle = np.radians(angle)
            result = np.sin(angle)
            return f"{result.round(2)}"
        return f"{self.fraction_decimal_conversion(np.sin(angle))} radians"

    def sininverse(self, num):
        num = float(num)
        # we need to convert radians to angle at the end
        if 1 >= num >= -1:
            angle1 = np.arcsin(num)
            if self.angle_mode == 'degrees':
                return f"{np.round(np.degrees(angle1), self.rounded)}°"
            return f"{angle1} radians"
        else:
            return "Error! Range must be between 1 and -1"

    # CONTINUE FROM HERE

    def cosinverse(self, num):
        num = float(num)
        if 1 >= num >= -1:
            angle1 = np.arccos(num)
            if self.angle_mode == 'degrees':
                return f"{np.round(np.degrees(angle1), self.rounded)}°"
            return f"{angle1} radians"
        else:
            return "Range must be between 1 and -1"

    def taninverse(self, num):
        num = float(num)
        try:
            angle1 = np.arctan(num)
            if self.angle_mode == 'degrees':
                return f"{np.round(np.degrees(angle1), self.rounded)}°"
            return f"{angle1} radians"
        except Exception as E:
            return "Error!"

    def cos(self, angle):
        # we need to convert angle to radians cuz thats what numpy expects
        if self.angle_mode == 'degrees':
            # angle = np.round(np.radians(angle), self.rounded)
            # return f"{angle}"
            angle = np.radians(angle)
            result = np.cos(angle)
            return f"{result.round(2)}"
        return f"{self.fraction_decimal_conversion(np.cos(angle))} radians"

    def tan(self, angle):
        # we need to convert angle to radians cuz thats what numpy expects
        if self.angle_mode == 'degrees':
            # angle = np.round(np.radians(angle), self.rounded)
            # return f"{angle}"
            angle = np.radians(angle)
            result = np.tan(angle)
            return f"{result.round(2)}"
        return f"{self.fraction_decimal_conversion(np.sin(angle))} radians"

    def log(self, num):
        if num > 0:
            return np.log10(num)
        else:
            return "Value cannot be less than 1"

    def ln(self, num):
        if num > 0:
            return np.log(num)
        else:
            return "Value cannot be less than 1"



# ------------------------------------




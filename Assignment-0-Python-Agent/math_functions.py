""" File name:   math_functions.py
    Author:      Taku Ueki
    Date:        23/02/17
    Description: This file defines a set of variables and simple functions.

                 It should be implemented for Exercise 1 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""
import math
ln_e = math.log(math.e)

twenty_radians = math.radians(20)

def quotient_ceil(numerator, denominator):
    return int(numerator//denominator + 1)

def quotient_floor(numerator, denominator):
    return int(numerator//denominator)

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

print(quotient_ceil(21, 5.3))

print(quotient_floor(21, 5.3))

print(manhattan(0,0,10,10))

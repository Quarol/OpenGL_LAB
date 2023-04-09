import random
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def renderRectangle(time, x, y, xLength: int, yLength: int, colorRGB = [1.0, 1.0, 1.0]):

    if abs(x) + xLength/2 > 100 or abs(y) + yLength/2 > 100:
        glfwTerminate()
        print("Wrong input: the figure exceeds the window border(s)")
        sys.exit(-1)

    glColor3f(colorRGB[0], colorRGB[1], colorRGB[2])

    glBegin(GL_TRIANGLE_STRIP)
    glVertex2f(x + xLength/2, y - yLength/2)
    glVertex2f(x - xLength/2, y - yLength/2)
    glVertex2f(x + xLength/2, y + yLength/2)
    glVertex2f(x - xLength/2, y + yLength/2)
    glEnd()


def renderRow(time, x, y, xLength, yLength, powerOf3, colorRGB = [1.0, 1.0, 1.0]):
    initialX = x

    for i in range(powerOf3):
        for i in range(powerOf3):
            renderRectangle(time, x, y, xLength/3, yLength/3)
            x += xLength
        x = initialX
        y -= yLength


def render(time, x, y, xLength: int, yLength: int, presicion: int):
    glClear(GL_COLOR_BUFFER_BIT)
    renderRectangle(time, x, y, xLength, yLength, [1.0, 0.0, 0.0])

    powerOf3 = 1
    for i in range(presicion):
        renderRow(time, x, y, xLength, yLength, powerOf3)
        xLength /= 3
        yLength /= 3
        x -= xLength
        y += yLength
        powerOf3 *= 3

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), 0, 0, 180, 180, 5)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()


import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time, x, y, xLength: int, yLength: int):

    if abs(x) + xLength/2 > 100 or abs(y) + yLength/2 > 100:
        glfwTerminate()
        print("Wrong input: the figure exceeds the window border(s)")
        sys.exit(-1)

    a = [x - xLength/2, y - yLength/2]
    b = [x + xLength/2, y - yLength/2]
    c = [x + xLength/2, y + yLength/2]
    d = [x - xLength/2, y + yLength/2]

    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(a[0], a[1])
    glVertex2f(b[0], b[1])
    glVertex2f(d[0], d[1])
    glEnd()


    glBegin(GL_TRIANGLES)
    glVertex2f(d[0], d[1])
    glVertex2f(c[0], c[1])
    glVertex2f(b[0], b[1])
    glEnd()
    glFlush()


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
        render(glfwGetTime(), 8, -80, 180, 34)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

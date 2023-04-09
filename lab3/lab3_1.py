import sys
import math
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
   glRotatef(angle, 1.0, 0.0, 0.0)
   glRotatef(angle, 0.0, 1.0, 0.0)
   glRotatef(angle, 0.0, 0.0, 1.0)


def render(time, vertices : list, X : int, Y : int):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / math.pi)
    axes()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for i in range(X):
        for j in range(Y):
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

    glEnd()

    glFlush()

def x(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.cos(math.pi*v)

def y(u):
    return 160*pow(u, 4) - 320*pow(u, 3) + 160*pow(u, 2) - 5

def z(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.sin(math.pi*v)


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def initializeVertices(N : int):
    nQuantum = 1.0/(N-1)
    uValues = []
    vValues = []
    fValues = [[[0] * 3 for i in range(N)] for j in range(N)]

    uValues.append(0.0)
    vValues.append(0.0)
    for i in range(1, N-1):
        uValues.append( i*nQuantum )
        vValues.append( i*nQuantum )
    uValues.append(1.0)
    vValues.append(1.0)

    for i in range(N):
        for j in range(N):
                fValues[i][j][0] = x(uValues[i], vValues[j])
                fValues[i][j][1] = y(uValues[i])
                fValues[i][j][2] = z(uValues[i], vValues[j])

    return fValues


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

    N = 31
    vertices = initializeVertices(N)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertices, N, N)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

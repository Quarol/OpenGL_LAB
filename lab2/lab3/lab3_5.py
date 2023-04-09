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

def renderSun(gravityCenter, radius, N):
    uValues = []   # pionowo
    vValues = []   # poziomo
    for i in range(N):
        uValues.append(i/(N-1))
        vValues.append(i/(N-1))
    
    sunPoints = [[[0] * 3 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            sunPoints[i][j][0] = gravityCenter[0] + radius * math.cos(2*math.pi * uValues[i]) * math.cos(2*math.pi * vValues[j])
            sunPoints[i][j][1] = gravityCenter[1] + radius * math.sin(2*math.pi  * vValues[j])
            sunPoints[i][j][2] = gravityCenter[2] + radius * math.sin(2*math.pi * uValues[i]) * math.cos(2*math.pi * vValues[j])

    glColor3f(1.0, 1.0, 0.0) #yellow
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N):
        for j in range(N):
            glVertex3f(sunPoints[i][j][0], sunPoints[i][j][1], sunPoints[i][j][2])

            if i+1 < N:
                glVertex3f(sunPoints[i+1][j][0], sunPoints[i+1][j][1], sunPoints[i+1][j][2])
    glEnd()


def renderPlanet(time, deltaTime, elipsePoints, radius, N):
    global index
    uValues = []   # pionowo
    vValues = []   # poziomo
    for i in range(N):
        uValues.append(i/(N-1))
        vValues.append(i/(N-1))
    
    planetPoints = [[[0] * 3 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            planetPoints[i][j][0] = radius * math.cos(2*math.pi * uValues[i]) * math.cos(2*math.pi * vValues[j])
            planetPoints[i][j][1] = radius * math.sin(2*math.pi  * vValues[j])
            planetPoints[i][j][2] = radius * math.sin(2*math.pi * uValues[i]) * math.cos(2*math.pi * vValues[j])

    glColor3f(0.8, 0.5, 0.1) #sth like orange
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N):
        for j in range(N):

            glVertex3f(planetPoints[i][j][0] + elipsePoints[index][0],
             planetPoints[i][j][1] + elipsePoints[index][1],
              planetPoints[i][j][2])

            if i+1 < N:
                glVertex3f(planetPoints[i+1][j][0] + elipsePoints[index][0],
                 planetPoints[index][j][1] + elipsePoints[index][1],
                  planetPoints[i][j][2])
    glEnd()

    index += 1
    if index == N:
        index = 0

index = 0

def renderElipse(maxRadius, minRadius, N):
    glColor3f(1.0, 1.0, 1.0) #white

    uValues = []   # pionowo
    for i in range(N):
        uValues.append(i/(N-1))
    
    elipsePoints = [[0] * 2 for i in range(N)]
    for i in range(N):
            elipsePoints[i][0] = maxRadius * math.cos(2*math.pi * uValues[i])
            elipsePoints[i][1] = minRadius * math.sin(2*math.pi * uValues[i])

    glBegin(GL_LINE_LOOP)
    for i in range(N):
        glVertex3f(elipsePoints[i][0], elipsePoints[i][1], 0.0)
    glEnd()

    return elipsePoints


def renderSolarSystem(time):
    maxRadius = 7.5
    minRadius = 4.5
    F1 = (-3.5, 0.0, 0.0) #Sun
    F2 = (3.5, 0.0, 0.0)

    N = 30
    elipsePoints = renderElipse(maxRadius, minRadius, N)
    renderSun(F1, 0.5, N)
    renderPlanet(time, glfwGetTime() - time, elipsePoints, 0.3, N)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 45 / math.pi)
    axes()

    renderSolarSystem(time)

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

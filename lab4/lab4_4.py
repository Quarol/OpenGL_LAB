import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

pix2angle = 1.0
R = viewer[2]
R_MAX = 20
R_MIN = 4.0
scale = 1.0
sensitivity = 1/100

theta = 0.0
phi = 0.0
radPhi = 0.0
radTheta = 0.0
xEye = 0.0
yEye = 0.0
zEye = 0.0
yValue = 1.0

isRotatingOn = False
right_mouse_button_pressed = False
left_mouse_button_pressed = False

mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0



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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta, phi
    global radPhi, radTheta
    global scale
    global delta_x, delta_y
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global sensitivity
    global R
    global xEye, yEye, zEye, yValue

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

        if theta is not 360:
            theta %= 360
        if phi is not 360:
            phi %= 360

    if right_mouse_button_pressed:
        tempR = R + delta_x * sensitivity * pix2angle

        if tempR >= R_MIN and tempR <= R_MAX:
            R = tempR
            scale = 1/tempR * viewer[2]

    
    if isRotatingOn:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
    
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        glScalef(scale, scale, scale)
    
    else:
        radPhi = phi * math.pi/180 
        radTheta = theta * math.pi/180
        xEye = R * math.cos(radTheta) * math.cos(radPhi)
        yEye = R * math.sin(radPhi)
        zEye = R * math.sin(radTheta) * math.cos(radPhi)

        if phi >= 90 and phi <= 270:
            yValue = -1
        else:
            yValue = 1

        gluLookAt(xEye, yEye, zEye,
                  0.0, 0.0, 0.0,
                  0.0, yValue, 0.0)

    

    example_object()
    axes()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global isRotatingOn
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        isRotatingOn = not isRotatingOn
        print(isRotatingOn)



def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = True
    else:
        right_mouse_button_pressed = False

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = True
    else:
        left_mouse_button_pressed = False

def main():
    if not glfwInit():
        sys.exit(-1)

    print(isRotatingOn)
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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

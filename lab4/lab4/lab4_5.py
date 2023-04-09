import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 11.0]

pix2angle = 1.0
R = viewer[2]
R_MAX = 20
R_MIN = 4.0
scale = 1.0
sensitivity = 1/100
moveSpeed = 1/100

theta = 90.0
phi = 0.0
radPhi = phi * math.pi/180 
radTheta = theta * math.pi/180

xEye = R * math.cos(radTheta) * math.cos(radPhi)
yEye = R * math.sin(radPhi)
zEye = R * math.sin(radTheta) * math.cos(radPhi)

xAt = 0.0
yAt = 0.0
zAt = 0.0

xUp = 0.0
yUp = 1.0
zUp = 0.0

T_x = 0.0
T_y = 0.0
T_z = 0.0
verticalShift  = 0.0
horizontalShift = 0.0

xDir = 1.0
yDir = 1.0
zDir = 1.0

w_pressed = False
d_pressed = False
s_pressed = False
a_pressed = False

left_mouse_button_pressed = False
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

shift = [0.0, 0.0, 0.0]
timeWhenPressed = 0.0

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
    global sensitivity
    global R
    global xEye, yEye, zEye
    global T_x, T_y, T_z
    global horizontalShift, verticalShift
    global xUp, yUp, zUp
    global xAt, yAt, zAt
    global xDir, yDir, zDir
    global shift

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

        theta %= 360
        phi %= 360

    if phi >= 90 and phi <= 270:
        yDir = -1
        yUp = yDir
    else:
        yDir = 1
        yUp = yDir

    if theta >= 90 and theta <= 270:
        xDir = -1
    else:
        xDi = 1

    radPhi = phi * math.pi/180 
    radTheta = theta * math.pi/180
    xAt = R * math.cos(radTheta) * math.cos(radPhi)
    yAt = R * math.sin(radPhi) * -1
    zAt = R * math.sin(radTheta) * math.cos(radPhi)

    x = xAt - xEye
    y = yAt - yEye
    z = zAt - zEye

    if w_pressed:
        shift[0] -= x * moveSpeed
        shift[1] -= y    * moveSpeed
        shift[2] -= z * moveSpeed

        verticalShift -= moveSpeed * yUp
    
    if s_pressed:
        shift[0] += x * moveSpeed
        shift[1] += y    * moveSpeed
        shift[2] += z * moveSpeed
        verticalShift += moveSpeed * yUp

    if a_pressed:
        shift[0] -= (yUp * z - zUp * y)    * moveSpeed
        shift[1] -= (zUp * x - xUp * z)    * moveSpeed
        shift[2] -= (xUp * y - yUp * x)    * moveSpeed
        verticalShift += moveSpeed * yUp

    if d_pressed:
        shift[0] += (yUp * z - zUp * y)    * moveSpeed
        shift[1] += (zUp * x - xUp * z)    * moveSpeed
        shift[2] += (xUp * y - yUp * x)    * moveSpeed
        verticalShift += moveSpeed * yUp


    gluLookAt(xEye, yEye, zEye,
              xAt, yAt, zAt,
              xUp, yUp, zUp)

    T_x = horizontalShift
    T_y = verticalShift
    
    #glTranslate(T_x, T_y, T_z)
    glTranslate(shift[0], shift[1], shift[2])


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
    global w_pressed
    global s_pressed
    global a_pressed
    global d_pressed
    global timeWhenPressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_W and (action == GLFW_PRESS or action == GLFW_REPEAT):
        w_pressed = True
    if key == GLFW_KEY_W and action == GLFW_RELEASE:
        w_pressed = False

    if key == GLFW_KEY_S and (action == GLFW_PRESS or action == GLFW_REPEAT):
        s_pressed = True
    if key == GLFW_KEY_S and action == GLFW_RELEASE:
        s_pressed = False

    if key == GLFW_KEY_A and (action == GLFW_PRESS or action == GLFW_REPEAT):
        a_pressed = True
    if key == GLFW_KEY_A and action == GLFW_RELEASE:
        a_pressed = False

    if key == GLFW_KEY_D and (action == GLFW_PRESS or action == GLFW_REPEAT):
        d_pressed = True
    if key == GLFW_KEY_D and action == GLFW_RELEASE:
        d_pressed = False


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = True
    else:
        left_mouse_button_pressed = False

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
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

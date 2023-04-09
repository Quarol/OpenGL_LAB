import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]
theta = 0.0
phi = 0.0
pix2angle = 1.0
movement_speed = 1/20

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [5.0, 0.0, 0.0, 1.0]

light_ambient1 = [0.1, 0.1, 0.0, 1.0]
light_diffuse1 = [0.9, 0.0, 0.5, 1.0]
light_specular1 = [1.0, 0.0, 0.0, 1.0]
light_position1 = [-5.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def addLight(GL_LIGHT, mat_ambient, mat_diffuse, mat_specular, mat_shininess,
             light_ambient, light_diffuse, light_specular, light_position):

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glLightfv(GL_LIGHT, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT, GL_POSITION, light_position)

    glLightf(GL_LIGHT, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    addLight(GL_LIGHT0, mat_ambient, mat_diffuse, mat_specular, mat_shininess,
    light_ambient, light_diffuse, light_specular, light_position)

    addLight(GL_LIGHT1, mat_ambient, mat_diffuse, mat_specular, mat_shininess,
    light_ambient1, light_diffuse1, light_specular1, light_position1)


def shutdown():
    pass


def draw_light_source(position):

    glTranslate(position[0], position[1], position[2])

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 1, 6, 2)
    gluDeleteQuadric(quadric)

    glTranslate(-position[0], -position[1], -position[2])


def calc_light_position(position, radius, phi, theta, name):
    position[0] = radius * math.cos(theta) * math.cos(phi)
    position[1] = radius * math.sin(phi)
    position[2] = radius * math.sin(theta) * math.cos(phi)
    glLightfv(name, GL_POSITION, position)

def spin(angle):
   glRotatef(angle, 1.0, 0.0, 0.0)
   glRotatef(angle, 0.0, 1.0, 0.0)
   glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    global theta, phi
    global light_position, light_position1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * movement_speed
        phi += delta_y * pix2angle * movement_speed

        theta %= 360
        phi %= 360 

        calc_light_position(light_position, 5, phi, theta, GL_LIGHT0)
        calc_light_position(light_position1, 5, phi + math.pi, theta, GL_LIGHT1)


    draw_light_source(light_position1)
    draw_light_source(light_position)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

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

################### COLOR CHANGE
option_keys_dict = {
                    GLFW_KEY_N : 0,
                    GLFW_KEY_1 : [0, light_ambient],
                    GLFW_KEY_2 : [1, light_ambient],
                    GLFW_KEY_3 : [2, light_ambient],
                    GLFW_KEY_4 : [0, light_diffuse],
                    GLFW_KEY_5 : [1, light_diffuse],
                    GLFW_KEY_6 : [2, light_diffuse],
                    GLFW_KEY_7 : [0, light_specular],
                    GLFW_KEY_8 : [1, light_specular],
                    GLFW_KEY_9 : [2, light_specular]
                    }

selected_option = GLFW_KEY_N
change = 0.1

def change_value(change : int, index_and_paramater : list):
    global light_ambient, light_diffuse, light_specular

    index = index_and_paramater[0]
    parameter = index_and_paramater[1]
    newValue = parameter[index] + change

    if newValue >= 0.0 and newValue <= 1.0:
        parameter[index] = newValue

    startup()



def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    global selected_option
    if action == GLFW_PRESS and key in option_keys_dict:
        selected_option = key

    if selected_option != GLFW_KEY_N:

        if action == GLFW_PRESS and key == GLFW_KEY_UP:
            change_value(change, option_keys_dict[selected_option])

        if action == GLFW_PRESS and key == GLFW_KEY_DOWN:
            change_value(-change, option_keys_dict[selected_option])
        


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

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0



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

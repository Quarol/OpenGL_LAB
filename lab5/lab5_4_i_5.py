import sys
import random
import math
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

drawNormals = False


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


def render(time, vertices : list, normals : list, N : int):
    global theta, phi
    global light_position, light_position1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #gluLookAt(viewer[0], viewer[1], viewer[2],
              #0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * movement_speed
        phi += delta_y * pix2angle * movement_speed

        theta %= 360
        phi %= 360 

        calc_light_position(light_position, 8.5, phi, theta, GL_LIGHT0)
        calc_light_position(light_position1, 8.5, phi + math.pi, theta, GL_LIGHT1)


    draw_light_source(light_position1)
    draw_light_source(light_position)


    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

            if i + 1 < N:
                glNormal3f(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
                glVertex3f(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])

        glEnd()



    if drawNormals:
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                vector = normals[i][j]

                if i > N/2 -1:
                    vector[0] = -vector[0]
                    vector[1] = -vector[1]
                    vector[2] = -vector[2] 

                second_vector = normal_top(vector, vertices[i][j])

                glNormal3fv(second_vector)
                glVertex3fv(second_vector)

                glNormal3fv(vector)
                glVertex3fv(vector)
        glEnd()


    glFlush()


def normal_top(point, vector):
    x = point[0] + vector[0]
    y = point[1] + vector[1]
    z = point[2] + vector[2]
    return [x, y, z]


#Coordinates:
def x(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.cos(math.pi*v)

def y(u, v):
    return 160*pow(u, 4) - 320*pow(u, 3) + 160*pow(u, 2) - 5

def z(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.sin(math.pi*v)
#

#Differentian coordinates:
def calc_xu(u, v):
    return (-450*u**4 + 900*u**3 - 810*u**2 + 360*u - 45) * math.cos(math.pi * v)

def calc_xv(u, v):
    return math.pi * (90*u**5 - 225*u**4 + 270*u**3 - 180*u**2 + 45*u) * math.sin(math.pi * v)

def calc_yu(u, v):
    return 640*u**3 - 960*u**2 + 320*u

def calc_yv(u, v):
    return 0

def calc_zu(u, v):
    return (-450*u**4 + 900*u**3 - 810*u**2 + 360*u - 45) * math.sin(math.pi * v)

def calc_zv(u, v):
    return -math.pi * (90*u**5 - 225*u**4 + 270*u**3 - 180*u**2 + 45*u) * math.cos(math.pi * v)
#


def calc_normal(u, v):
    xu = calc_xu(u, v)
    xv = calc_xv(u, v)

    yu = calc_yu(u, v)
    yv = calc_yv(u, v)
    
    zu = calc_zu(u, v)
    zv = calc_zv(u, v)

    return [yu*zv - zu*zv,
            zu*xv - xu*zv,
            xu*yv - yu*xv]


def initializeNormals(N : int):
    nQuantum = 1.0/(N-1)
    uValues = []
    vValues = []
    normals = [[[0] * 3 for i in range(N)] for j in range(N)]

    uValues.append(0.0)
    vValues.append(0.0)
    for i in range(1, N-1):
        uValues.append( i*nQuantum )
        vValues.append( i*nQuantum )
    uValues.append(1.0)
    vValues.append(1.0)


    for i in range(N):
        for j in range(N):
            normal = calc_normal(uValues[i], vValues[j])
            normals[i][j] = normalizeVector(normal)

    return normals



def normalizeVector(vector : list):
    d = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

    if d == 0:
        return [0, 0, 0]

    x = vector[0] / d
    y = vector[1] / d
    z = vector[2] / d

    return [x, y, z]    


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
                fValues[i][j][1] = y(uValues[i], vValues[j])
                fValues[i][j][2] = z(uValues[i], vValues[j])

    return fValues


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

def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    global drawNormals
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        drawNormals = not drawNormals


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


    N = 17
    vertices = initializeVertices(N)
    normals = initializeNormals(N)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertices, normals, N)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

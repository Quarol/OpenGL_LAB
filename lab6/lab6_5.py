import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = False

mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

uValues = []
vValues = []


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("tekstura.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
      


def shutdown():
    pass



def render(time, vertices : list, N : int):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)  


    #glTexCoord2f(vertices[i][j][0], vertices[i][j][1])
    #glTexCoord2f(vertices[i+1][j][0], vertices[i+1][j][1])
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            if i > N/2 -1:    
                glTexCoord2f(uValues[i+1], vValues[j])
                glVertex3f(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])

                glTexCoord2f(uValues[i], vValues[j])
                glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            else:
                glTexCoord2f(uValues[i], vValues[j])
                glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

                glTexCoord2f(uValues[i+1], vValues[j])
                glVertex3f(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
                
        glEnd()


    glFlush()

def x(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.cos(math.pi*v)

def y(u):
    return 160*pow(u, 4) - 320*pow(u, 3) + 160*pow(u, 2) - 5

def z(u, v):
    return (-90*pow(u, 5) + 225*pow(u, 4) - 270*pow(u, 3) + 180*pow(u, 2) - 45*u) * math.sin(math.pi*v)


def initializeVertices(N : int):
    global uValues, vValues

    nQuantum = 1.0/(N-1)
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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


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
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    N = 31
    vertices = initializeVertices(N)
    

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertices, N)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
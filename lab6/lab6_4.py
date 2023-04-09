import sys
import os

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0

mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

tex1 = Image.open("byniu.tga")
tex2 = Image.open("qubic.tga")
tex1_set = True

def setTex(image):
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


def shutdown():
    pass


def render_square():
    glBegin(GL_TRIANGLE_FAN)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(3.0, -3.0, -3.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, -3.0, 3.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(-3.0, -3.0, 3.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, -3.0)

    
    glEnd()


def render_triangle(x0, y0, z0,
                    x1, y1, z1,
                    x2, y2, z2):
    glBegin(GL_TRIANGLES)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(x0, y0, z0)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x1, y1, z1)
    
    glTexCoord2f(0.5, 1.0)
    glVertex3f(x2, y2, z2)

    glEnd()


def play_song():
    os.startfile("inz.mp3")

def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

        theta %= 360
        phi %= 360

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    
    if tex1_set:
        setTex(tex1)
    else:
        setTex(tex2)

    render_square()
    render_triangle(-3.0, -3.0, 3.0,
                    3.0, -3.0, 3.0,
                    0.0, 3.0, 0.0)
    render_triangle(3.0, -3.0, 3.0,
                    3.0, -3.0, -3.0,
                    0.0, 3.0, 0.0)
    render_triangle(-3.0, -3.0, -3.0,
                    -3.0, -3.0, 3.0,
                    0.0, 3.0, 0.0)
    render_triangle(3.0, -3.0, -3.0,
                    -3.0, -3.0, -3.0,
                    0.0, 3.0, 0.0)


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
    global tex1_set

    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        tex1_set = True
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        tex1_set = False

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

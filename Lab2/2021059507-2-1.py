import glfw
from OpenGL.GL import *
import numpy as np

number = 4

def compute_vertices(v_num):
    angles = np.linspace(0, 2*np.pi,v_num, endpoint=False)

    x_coordinates = np.cos(angles)
    y_coordinates = np.sin(angles)

    vertices = np.column_stack((x_coordinates, y_coordinates))

    return vertices

def render(vertices, key):
    if(key==1):
        glBegin(GL_POINTS)
    elif(key==2):
        glBegin(GL_LINES)
    elif(key==3):
        glBegin(GL_LINE_STRIP)
    elif(key==4):
        glBegin(GL_LINE_LOOP)
    elif(key==5):
        glBegin(GL_TRIANGLES)
    elif(key==6):
        glBegin(GL_TRIANGLE_STRIP)
    elif(key==7):
        glBegin(GL_TRIANGLE_FAN)
    elif(key==8):
        glBegin(GL_QUADS)
    elif(key==9):
        glBegin(GL_QUAD_STRIP)
    elif(key==0):
        glBegin(GL_POLYGON)

    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global number
    if action == glfw.PRESS:
        if key == glfw.KEY_0:
            number = 0
        elif key == glfw.KEY_1:
            number = 1
        elif key == glfw.KEY_2:
            number = 2
        elif key == glfw.KEY_3:
            number = 3
        elif key == glfw.KEY_4:
            number = 4
        elif key == glfw.KEY_5:
            number = 5
        elif key == glfw.KEY_6:
            number = 6
        elif key == glfw.KEY_7:
            number = 7
        elif key == glfw.KEY_8:
            number = 8
        elif key == glfw.KEY_9:
            number = 9

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2021059507-2-1", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -1.0)
        glColor3f(1.0, 1.0, 1.0)

        vertices = compute_vertices(12)
        render(vertices,number)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

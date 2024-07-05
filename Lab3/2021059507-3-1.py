import glfw
from OpenGL.GL import *
import numpy as np

key_in = None #keyboard input

global gComposedM
gComposedM = np.array([[1., .0, .0],
                       [.0, 1., .0],
                       [.0, .0, 1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    #draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0, .5, 1.])) [:-1] )
    glVertex2fv( (T @ np.array([.0, .0, 1.])) [:-1] )
    glVertex2fv( (T @ np.array([.5, .0, 1.])) [:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global key_in
    global gComposedM
    if action == glfw.PRESS:
        if key == glfw.KEY_Q:
            newM = np.array([[1., .0, -0.1],
                             [.0, 1., .0],
                             [.0, .0, 1.]])
            gComposedM = newM @ gComposedM

        elif key == glfw.KEY_E:
            newM = np.array([[1., .0, .1],
                            [.0, 1., .0],
                            [.0, .0, 1.]])
            gComposedM = newM @ gComposedM

        elif key == glfw.KEY_A:
            newM = np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10)), .0],
                             [np.sin(np.radians(10)), np.cos(np.radians(10)), .0],
                             [.0, .0, 1.]])
            gComposedM = gComposedM @ newM

        elif key == glfw.KEY_D:
            newM = np.array([[np.cos(np.radians(10)), np.sin(np.radians(10)), .0],
                             [-np.sin(np.radians(10)), np.cos(np.radians(10)), .0],
                             [.0, .0, 1.]])
            gComposedM = gComposedM @ newM

        elif key == glfw.KEY_1:
            gComposedM = np.array([[1., .0, .0],
                             [.0, 1., .0],
                             [.0, .0, 1.]])

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2021059507-3-1", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

from typing import Optional

import glfw
from OpenGL.GL import *
from glfw.GLFW import *

from game.ecs.component.motion import Velocity
from game.world.generator import generate_world


# from gfx import Shader
# from gfx import Texture


# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------
def process_keyboard_input(window) -> Optional[Velocity]:
    player_velocity = Velocity(0.0, 0.0, 0.0)

    if glfw.get_key(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)
        return None

    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        player_velocity.y = 0.5

    if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        player_velocity.y = -0.5

    if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        player_velocity.x = -0.5

    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        player_velocity.x = 0.5

    return player_velocity


def render_loop(window):
    world, player = generate_world(10, 10)

    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

    last_frame_time = glfw.get_time()

    while not glfw.window_should_close(window):
        # input
        # -----
        player_velocity = process_keyboard_input(window)

        # render
        # ------
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        current_frame_time = glfw.get_time()
        delta_time = current_frame_time - last_frame_time
        last_frame_time = current_frame_time

        if player_velocity is not None:
            world.remove_component(player, Velocity)
            world.add_component(player, player_velocity)

        world.process(delta_time)

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        # -------------------------------------------------------------------------------
        glfw.swap_buffers(window)
        glfw.poll_events()


# glfw: whenever the window size changed (by OS or user resize) this callback function executes
# ---------------------------------------------------------------------------------------------
def framebuffer_size_callback(window: glfw._GLFWwindow, width: int, height: int) -> None:
    # make sure the viewport matches the new window dimensions note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Logo Maze game", None, None)

    if window is None:
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    render_loop(window)

    pass


if __name__ == '__main__':
    main()




import os
from concurrent.futures import ProcessPoolExecutor
from itertools import cycle
from typing import Optional

import esper
import glfw
import glm
import pygame
from pygame.mixer import music
from OpenGL.GL import *
from glfw.GLFW import *

from game.ecs.component.motion import Velocity
from game.world.generator import generate_world

projection = None
regenerate_world = False


def mouse_button_callback(window, button, action, mods):
    if action == GLFW_PRESS:
        x, y = glfw.get_cursor_pos(window)

        global projection

        viewport = glGetIntegerv(GL_VIEWPORT)

        viewport = glm.vec4(viewport)

        clip_coordinates = glm.unProject(glm.vec3(x, y, 0.0), glm.identity(glm.mat4), projection, viewport)

        esper.dispatch_event("mouse_click", clip_coordinates[0], clip_coordinates[1], button)

        pass



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
    world_x = world_y = 10

    (world, world_size), player = generate_world(world_x, world_y)

    global projection
    projection = world_size

    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

    last_frame_time = glfw.get_time()

    def regenerate_world_handler(_):
        global regenerate_world
        regenerate_world = True

    esper.set_handler("regenerate_world", regenerate_world_handler)

    while not glfw.window_should_close(window):
        global regenerate_world
        if regenerate_world:
            regenerate_world = False
            (world, world_size), player = generate_world(world_x, world_y)

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


def play_soundtrack(sounds_path: str):
    pygame.mixer.init()
    pygame.init()

    songs = map(lambda f: os.path.join(sounds_path, f), os.listdir(sounds_path))
    songs = filter(os.path.isfile, songs)
    songs = list(songs)
    songs_cycle = cycle(songs)

    music.load(next(songs_cycle))
    music.queue(next(songs_cycle))
    music.set_endevent(pygame.USEREVENT)
    music.set_volume(0.2)
    music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # A track has ended
                pygame.mixer.music.queue(next(songs_cycle))  # Queue the next one in the list


def main():
    glfw.init()
    window = glfw.create_window(1280, 1280, "Logo Maze game", None, None)

    if window is None:
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1

    executor = ProcessPoolExecutor()
    executor.submit(play_soundtrack, 'game/songs')
    executor.shutdown(wait=False)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    render_loop(window)

    pass


if __name__ == '__main__':
    main()




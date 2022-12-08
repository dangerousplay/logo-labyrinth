
from typing import Any

import imgui
import esper
import moderngl
import moderngl_window as mglw
import pygame.time
from moderngl_window.context.base import KeyModifiers
from moderngl_window.scene import KeyboardCamera
from pyphysx import RigidDynamic
from pyphysx_render.pyrender import PyPhysxViewer
from pyrr import Matrix44, Vector3

from game.ecs.entity import light
from game.ecs.processor.keyboard import KeyboardProcessor
from game.world.generator import generate_world

from moderngl_window.integrations.imgui import ModernglWindowRenderer


class GameWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1920, 1080)
    title = "3D labyrinth"
    resource_dir = "resources"
    cursor = True

    menu_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = KeyboardCamera(self.wnd.keys, fov=60.0, aspect_ratio=self.wnd.aspect_ratio, near=0.1, far=1000.0)
        self.camera.dir = Vector3([3, 0, -1])
        self.camera.mouse_sensitivity = 0.1

        self.key_processor = KeyboardProcessor()

        esper.set_handler("regenerate_world", self._generate_world_)

        self._generate_world_()

        self.clock = pygame.time.Clock()

        imgui.create_context()

        self.mouse_exclusivity = True

        # self.physx_render = PyPhysxViewer()
        # self.physx_render.add_physx_scene(self.scene)

        self.imgui = ModernglWindowRenderer(self.wnd)

    def _generate_world_(self, *args):
        self.world, self.scene = generate_world(5, 5, self.camera)
        self.world.add_processor(self.key_processor)

        self.lights = []
        _, w_light = light.create(self.world, Vector3([0, 500, -400]))

        self.lights.append(w_light)

        _, w_light = light.create(self.world, Vector3([93, -15, 296]))

        self.lights.append(w_light)

    def render_ui(self):
        """Render the UI"""
        imgui.new_frame()

        imgui.begin("Camera", True)

        for pos, label in zip(self.camera.position, ['X', 'Y', 'Z']):
            imgui.text(f"{label}: {pos}")

        imgui.text(f"FPS: {self.clock.get_fps()}")

        imgui.end()

        self._render_light_ui()

        imgui.render()

        self.imgui.render(imgui.get_draw_data())

    def _render_light_ui(self):
        for i, light in enumerate(self.lights):
            position = light.position

            imgui.begin(f"Light {i+1}", True)

            updated_position = []

            for pos, label in zip(position, ['X', 'Y', 'Z']):
                _, value = imgui.slider_float(f"{label}", pos, -1000, 1000)
                updated_position.append(value)

            imgui.end()

            light.position = Vector3(updated_position)

    def key_event(self, key: Any, action: Any, modifiers: KeyModifiers):
        # self.camera.key_input(key, action, modifiers)
        self.key_processor.process_key(self.wnd.keys, key, action, modifiers)
        self.imgui.key_event(key, action, modifiers)

        if key == self.wnd.keys.TAB:
            if action == self.wnd.keys.ACTION_PRESS:
                self.menu_open = not self.menu_open

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        if not self.menu_open:
            self.camera.rot_state(-dx, -dy)

        self.imgui.mouse_position_event(x, y, dx, dy)

    def resize(self, width: int, height: int):
        self.imgui.resize(width, height)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, character):
        self.imgui.unicode_char_entered(character)

    def render(self, time, frametime):
        # This method is called every frame
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # self.ctx.cull_face = 'back'
        self.ctx.clear(0.5444, 0.62, 0.69)

        self.world.process(frametime, camera=self.camera, gl_context=self.ctx)

        self.wnd.use()
        self.render_ui()

        self.clock.tick()


def start():
    # Blocking call entering rendering/event loop
    mglw.run_window_config(GameWindow)

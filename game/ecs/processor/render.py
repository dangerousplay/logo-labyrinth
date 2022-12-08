from os.path import abspath

import esper
import numpy
from moderngl import Program, Context
from moderngl_window import resources
from moderngl_window.meta import TextureDescription, ProgramDescription
from moderngl_window.scene import MeshProgram, Camera
from pyphysx import RigidActor

from game.ecs.component.physics import Scale, swap_yz
from game.ecs.component.scene import Renderable, Mesh, Light

from pyrr import Matrix44, Vector4

DEFAULT_SCALE = Matrix44.from_scale([1.0, 1.0, 1.0])

REFLECTION_BUFFER_SIZE = (320, 180)
REFRACTION_BUFFER_SIZE = (1280, 720)


def load_texture(path: str):
    return resources.textures.load(
            TextureDescription(
                path=abspath(path),
            )
        )


def load_program(vertex_shader: str, fragment_shader: str):
    return resources.programs.load(
        ProgramDescription(vertex_shader=abspath(vertex_shader), fragment_shader=abspath(fragment_shader))
    )


def default_plane():
    return Vector4([0, 1, 0, 1])


class TextureProgram(MeshProgram):
    def __init__(self, program: Program):
        super().__init__(program)

    def draw(
        self,
        mesh,
        projection_matrix: numpy.ndarray = None,
        model_matrix: numpy.ndarray = None,
        camera_matrix: numpy.ndarray = None,
        time=0.0,
    ):
        mesh.material.mat_texture.texture.use()

        self.program["projectionMatrix"].write(projection_matrix)
        self.program["viewMatrix"].write(camera_matrix)
        self.program["transformationMatrix"].write(model_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if not mesh.attributes.get("TEXCOORD_0"):
            return None

        if mesh.attributes.get("COLOR_0"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class RenderProcessor(esper.Processor):

    def __init__(self, world, pipeline=None, water_render=None):
        if pipeline is None:
            pipeline = []

        self.pipeline = pipeline
        self.water_render = water_render
        self.world = world

        shader = load_program('resources/shaders/texture_vs.glsl', 'resources/shaders/texture_fs.glsl')
        self.mesh_shader = TextureProgram(program=shader)

        self.reflection_fbo = None
        self.refraction_fbo = None

    def process(self, time, camera: Camera, gl_context: Context, **kwargs):
        # self.reflection_fbo.clear()
        # self.reflection_fbo.use()
        #
        # camera_distance = 2 * camera.position[1]
        #
        # camera.pitch *= -1
        # camera.position[1] -= camera_distance

        self.render_scene(mesh_shader=self.mesh_shader, camera=camera, gl_context=gl_context)

        # camera.pitch *= -1
        # camera.position[1] += camera_distance
        #
        # current_fbo.use()
        # gl_context.fbo = current_fbo
        #
        # self.render_scene(mesh_shader=self.mesh_shader, camera=camera, gl_context=gl_context)

    def render_scene(self, camera: Camera, mesh_shader: MeshProgram, gl_context: Context, plane=default_plane()):

        for ent, (renderable, actor) in self.world.get_components(Mesh, RigidActor):
            renderable: Renderable = renderable
            scale = DEFAULT_SCALE

            if self.world.has_component(ent, Scale):
                scale = self.world.component_for_entity(ent, Scale).value

            actor: RigidActor
            position = Matrix44.from_translation(swap_yz(actor.get_global_pose()[0]), dtype='f4')
            shader = mesh_shader.program

            light_positions = []
            light_colour = []
            attenuation = []

            for _, [light] in self.world.get_components(Light):
                light_positions.append(light.position)
                light_colour.append(light.color)
                attenuation.append(light.attenuation)

            shader["lightPosition"] = light_positions
            shader["lightColour"] = light_colour
            shader["attenuation"] = attenuation
            # shader["plane"] = plane

            renderable.draw(
                projection_matrix=camera.projection.matrix,
                camera_matrix=camera.matrix * position * scale,
                program=mesh_shader,
            )


class WaterRender:
    def __init__(self, dudv_texture: str, normal_map: str, shader: Program):

        self.dudv = load_texture(dudv_texture)
        self.normal_map = load_texture(normal_map)
        self.shader = shader

        self.shader["dudvMap"] = self.dudv
        self.shader["normalMap"] = self.normal_map
        self.reflection_texture = None
        self.refraction_texture = None

    def render(self, camera: Camera):
        pass


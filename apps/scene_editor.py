from core.tools.imgui_tools import MeshEditor
# from core.tools.imgui_tools import ObjectSpawner
from core.tools.imgui_tools import LightSpawner
from core.rendering.utils import drag_object
from core.utils.math import Math

from core.light.light import Light
from core.material.lighted.flat import FlatMaterial
from core.material.lighted.phong import PhongMaterial
from core.material.lighted.lambert import LambertMaterial
from core.glsl.utils import ShaderType
from core.glsl.utils import edit_light_list,edit_light_summation
from core.meshes.terrain import InfiniteTerrainManager
from core.tools.imgui_tools import TerrainHandler

from core.tools.entity_spawner import SpawnController, ObjectFactory, ObjectSpawnerView
from core.tools.light_spawner import  LightFactory, LightSpawnerController,LightSpawnerView
from apps.base import BaseApp
import imgui
import glfw
from core.components.types import Components
from core.entity import Entity

"""
    SceneEditor class for creating and editing 3D objects in a scene.
    Inherits from the BaseApp class.
    This class provides functionality for object creation, mesh editing,
    and rendering the scene with a camera.
    It uses ImGui for the user interface and GLFW for window management.
"""
class SceneEditor(BaseApp):
    def __init__(self, width=800, height=600,display_grid=True, static_camera=True,generate_terrain__at_start=False):
        super().__init__(title="SceneEditor", display_grid=display_grid, static_camera=static_camera, width=width, height=height)
        self._is_targetting_object = False
        self.disable_camera_rig = False
        self.draw_bbox = False
        self.selected_mesh= None
        self.menu_deadzones = []
        self.mesh_editor = MeshEditor()
        self.obj_maker = SpawnController(ObjectFactory(), ObjectSpawnerView())
        self.light_maker = LightSpawnerController(LightFactory(), LightSpawnerView(light_factory=LightFactory()))

        if  generate_terrain__at_start:
            # self.terrain_manager = InfiniteTerrainManager(chunk_size=100, view_distance=12, u_resolution=5, v_resolution=5)
            self.terrain_maker = TerrainHandler(chunk_size=100, view_distance=12, u_resolution=5, v_resolution=5)
            self.terrain_manager = self.terrain_maker.terrain_manager

        else:
            self.terrain_manager = None
            self.terrain_maker = None

    def update(self):

        imgui.begin("Scene Editor")

        # tab bar to hold the different tabs of the editor
        open_tab_bar = imgui.begin_tab_bar("MainTabBar")
        if open_tab_bar:
            
            ################### Main tab ###################
            if imgui.begin_tab_item("Meshes").selected:
                # # call object maker to allow the user to create objects
                obj = self.obj_maker.run()
                # if the user has created an object, add it to the scene
                if obj is not None:
                    self.scene.add(obj)
                
                # handle mesh editing
                if self._is_targetting_object and self.selected_mesh is not None:
                    self.mesh_editor.show()
                    self.disable_camera_rig = True

                # # check if the use wants to display bounding boxes
                # if self.obj_maker.show_bbox:
                #     self.draw_bbox = True
                #     self.renderer.enable_bound_box()
                # else:
                #     self.draw_bbox = False
                #     self.renderer.disable_bound_box()
                imgui.end_tab_item()

            ################### Lights tab ###################
            if imgui.begin_tab_item("Lights").selected:
                light_entity = self.light_maker.run()

                # if a new light is created, add it to the scene    
                if light_entity is not None:
                    self.scene.add(light_entity)
                    #update the light count in the scene
                    self.obj_maker.lights_in_scene = self.light_maker.count
                    self._update_lighted_meshes()

                imgui.end_tab_item()

            ################### Terrain tab ###################
            if imgui.begin_tab_item("Terrain").selected:
                # show the terrain manager
                # self.terrain_manager.update(self.camera.get_position())
                # self.terrain_manager.render(self.camera)
                # self.terrain_manager.show()
                
                # check if the user has set a terrain manager
                if self.terrain_manager is not None:
                    self.terrain_maker.show()
                    print("terrain manager settings:", self.terrain_manager.chunk_size, self.terrain_manager.view_distance, self.terrain_manager.u_resolution, self.terrain_manager.v_resolution)
                    if self.terrain_maker.update_terrain:
                    # if the user has updated the terrain manager, set it in the scene
                        self.terrain_manager = self.terrain_maker.terrain_manager
                        self.update_terrain = False
                    # self.set_terrain_manager(self.terrain_manager)

                imgui.end_tab_item()

            imgui.end_tab_bar()

        # update the renderer so it knows whether to use the lights in the scene or not
        if self.light_maker.use_lights:
            self.renderer.enable_lights = True
        else:
            self.renderer.enable_lights = False

        # calculate the bbox of the imgui menu
        widgect_pos = imgui.get_window_position()
        widgect_size = imgui.get_window_size()
        menu_deadzones = [widgect_pos[0], widgect_pos[1], widgect_size[0], widgect_size[1]]
        self.menu_deadzones = menu_deadzones

        imgui.end()
 

    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
        if not self.mesh_editor.editing_shader:
            self._handle_input()
         
         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)

             # handle mouse input
        if not Math.point_in_regions(self.input_handler.mouse_position, self.menu_deadzones):
            self._handle_mouse_input()
       

        #render the scene
        self.renderer.render(self.scene, self.camera,terrain_manager=self.terrain_manager)

    def _update_lighted_meshes(self):
        visible_meshes = self.scene.get_visible_objects()

        for mesh in visible_meshes:
            if isinstance(mesh,Entity):
                mesh = mesh.get_component(Components.MESH).mesh
            if isinstance(mesh.material, FlatMaterial):
               edit_light_list(mesh.material, self.light_maker.count,ShaderType.VERTEX)
               edit_light_summation(mesh.material, self.light_maker.count,ShaderType.VERTEX)

            if isinstance(mesh.material, LambertMaterial) or isinstance(mesh.material, PhongMaterial):
               edit_light_list(mesh.material, self.light_maker.count,ShaderType.FRAGMENT)
               edit_light_summation(mesh.material, self.light_maker.count,ShaderType.FRAGMENT)

            else:
                continue

            mesh.material.add_light_souces(self.light_maker.count)
            mesh.material.locate_uniforms()
            mesh.material.compile_shaders(mesh.material.vertex_shader, mesh.material.fragment_shader)
    
    def _handle_mouse_input(self):
         if self.input_handler.left_click() or self.input_handler.right_click():
        
            mesh_picked = self.scene.pick_object(self.input_handler.mouse_position, self.camera,width=self.window_width, height=self.window_height)
            
            if mesh_picked:
                self.selected_mesh = mesh_picked
                self._is_targetting_object = True
                
                # if the mesh is already selected
                if self.mesh_editor.mesh:
                    # if the user is holding shift, change the mesh
                    if self.input_handler.is_key_pressed(glfw.KEY_LEFT_SHIFT):
                        self.mesh_editor.change_mesh(self.selected_mesh)
                else: # if no mesh is selected, select the new one
                        self.mesh_editor.change_mesh(self.selected_mesh)

            if not mesh_picked and self.input_handler.right_click():
                self._is_targetting_object = False
                self.selected_mesh = None
                self.mesh_editor.change_mesh(None)
                self.disable_camera_rig = False
                
            if self.input_handler.left_click() and self.input_handler.mouse_held and mesh_picked:
                drag_object(mouse_position=self.input_handler.mouse_position, mesh=self.selected_mesh, camera=self.camera, 
                            width=self.window_width, height=self.window_height, input_handler=self.input_handler)
                
    def  set_terrain_manager(self, terrain_manager):
        """
        Set the terrain manager for the scene editor.
        This allows the scene editor to render terrain chunks.
        Args:
            terrain_manager (InfiniteTerrainManager): The terrain manager to set.
        """

        self.terrain_manager = terrain_manager
        print("Terrain manager set:", self.terrain_manager)
        # self.scene.add(self.terrain_manager)
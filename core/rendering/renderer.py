import OpenGL.GL as gl
from meshes.mesh import Mesh
from core.light.light import Light
from core.rendering.render_target import RenderTarget
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.light.shadow import Shadow

class Renderer(object):
    def __init__(self,clear_color:list = [0.0, 0.0, 0.],window_width:int=SCREEN_WIDTH,window_height:int = SCREEN_HEIGHT) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)
        # enables anti-aliasing
        gl.glEnable(gl.GL_MULTISAMPLE)

        # enables blending
        gl.glEnable(gl.GL_BLEND)
        # set the blending function
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # set the clear color
        gl.glClearColor(clear_color[0], clear_color[1], clear_color[2], 1.0)

        self.window_size = (window_width,window_height)

        self.shadows_enabled = False
        # self.shadow_object = None
        

    def render(self,scene:object,camera:object,clear_color:bool = True,clear_depth:bool = True,render_target:RenderTarget=None) -> None:
        # Filter descendents
        descendant_list = scene.descendant_list
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))
        
        # shadow pass
        if self.shadows_enabled:
          
            # self._shadow_object.render_target.height = self.window_size[1]
            # self._shadow_object.render_target.width = self.window_size[0]
            # Set render target properties
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._shadow_object.render_target.frame_buffer)
            gl.glViewport(0, 0, self._shadow_object.render_target.width, self._shadow_object.render_target.height)
            # # Set default color to white, used when no objects present to cast shadows
            # gl.glClearColor(1, 1, 1, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            # Everything in the scene gets rendered with depthMaterial so
            # only need to call glUseProgram & set matrices once
            gl.glUseProgram(self._shadow_object.material.program)
            self._shadow_object.update_internal()
            for mesh in mesh_list:
                # Skip invisible meshes
                if not mesh.visible:
                    continue
                # Only triangle-based meshes cast shadows
                if mesh.material.settings["draw_mode"] != gl.GL_TRIANGLES:
                    continue
                # Bind VAO
                gl.glBindVertexArray(mesh.vao_ref)
                # Update transform data
                self._shadow_object.material.uniforms["model_matrix"].data = mesh.global_matrix
                # Update uniforms (matrix data) stored in shadow material
                for var_name, uniform_obj in self._shadow_object.material.uniforms.items():
                    uniform_obj.upload_data()
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh.geometry.vertex_count)

    
        #update camera
        camera.update_view_matrix()

        kid_list = scene.descendant_list

        viewable_filter = lambda x: isinstance(x,Mesh) and x.visible

        light_filter = lambda x: isinstance(x,Light)

        viewable_meshes = list(filter(viewable_filter,kid_list))

        light_list = list(filter(light_filter,kid_list))

                # self.__create_shadow_map(viewable_meshes)
        # set the viewport to the size of the window
        if (render_target  == None):
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,0)
            gl.glViewport(0, 0, self.window_size[0], self.window_size[1])
        else: # set the viewport to the size of the render target
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,render_target.frame_buffer)
            gl.glViewport(0, 0, render_target.width, render_target.height)

        if clear_color:
            # clear the color buffer
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if clear_depth:
            # clear the depth buffer
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        for mesh in viewable_meshes:
            # install the program for the mesh
            gl.glUseProgram(mesh.material.program)
            # bind vertex array object for the mesh
            gl.glBindVertexArray(mesh.vao_ref)

            # ================== update the uniforms for the mesh not stored in the material ==================
            #update the model matrix based on the mesh's world matrix
            mesh.material.uniforms["model_matrix"].data = mesh.global_matrix

            # update the view matrix to match the camera
            mesh.material.uniforms["view_matrix"].data = camera.view_matrix

            # update the projection matrix to match the camera
            mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix

            # =========== Handle lights if any exist ==============
            # if the current mesh has a light material, update the light uniforms
            if "light_0" in mesh.material.uniforms.keys():
                number_of_lights = len(light_list) # number of lights in the scene
                for light_n in range(number_of_lights):
                    # check if the light exists in the material
                    light_name = "light_" + str(light_n) # figure out the name of the light
                    light_inst = light_list[light_n] # get the light instance from the list
            
                    #update the light uniforms in the material incase the light has changed
                    mesh.material.uniforms[light_name].data = light_inst

            # check if the mesh uses specular lighting
            if "view_position" in mesh.material.uniforms.keys():
                # update the view position to match the camera
                mesh.material.uniforms["view_position"].data = camera.global_position

            # check if the mesh uses shadows
            if self.shadows_enabled and "shadow_obj" in mesh.material.uniforms.keys():   
                mesh.material.uniforms["shadow_obj"].data = self.shadow_object  

            # ================== update the uniforms for the mesh stored in the material ==================
            for var_name,uniform_obj in mesh.material.uniforms.items():

                if uniform_obj.data is not None:
                    uniform_obj.upload_data()


            #update the render settings for the material
            mesh.material.update_render_settings()

            # draw the mesh
            gl.glDrawArrays(mesh.material.settings["draw_mode"],0,mesh.geometry.get_vertex_count())


    def update_window_size(self,window_width, window_height):
            self.window_size = (window_width, window_height)
    
    @property
    def shadow_object(self):
        return self._shadow_object

    def enable_shadows(self,shadow_light:Light,strenth:float = 0.5,resolution:list = [512,512]):
        self.shadows_enabled = True
        self._shadow_object = Shadow(light_source=shadow_light,resolution=resolution,strength=strenth)



    def __create_shadow_map(self,viewable_meshes:list[Mesh]):


        # need to create a shadow map for the light source of all viewable meshes
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,self.shadow_object.render_target.frame_buffer)
        gl.glViewport(0, 0, self.shadow_object.render_target.width, self.shadow_object.render_target.height)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # set up shadow map material for rendering
        gl.glUseProgram(self.shadow_object.material.program)

        self.shadow_object.update_internal()

        # iterate through all the viewable meshes and render them to the shadow map
        for mesh in viewable_meshes:
            #skip the mesh if it is not a shadow caster
            if mesh.material.settings["draw_style"] != gl.GL_TRIANGLES:
                continue
          
            gl.glBindVertexArray(mesh.vao_ref)

            self.shadow_object.material.uniforms["model_matrix"].data = mesh.get_world_matrix()

            for var_name,uniform_obj in self.shadow_object.material.uniforms.items():
                
                uniform_obj.upload_data()

            gl.glDrawArrays(gl.GL_TRIANGLES,0,mesh.geometry.get_vertex_count())


class QtRenderer(object):
    def __init__(self, clear_color: list = [0.0, 0.0, 0.0], window_width: int = SCREEN_WIDTH, window_height: int = SCREEN_HEIGHT, parent_widget=None) -> None:
        """
        Renderer class for rendering scenes.
        :param clear_color: Background color for the renderer.
        :param window_width: Width of the rendering window.
        :param window_height: Height of the rendering window.
        :param parent_widget: The parent QOpenGLWidget (TestWidget) to ensure context compatibility.
        """
        self.parent_widget = parent_widget  # Reference to the parent widget
        self.window_size = (window_width, window_height)
        self.shadows_enabled = False

        # Ensure the OpenGL context is current
        if self.parent_widget:
            self.parent_widget.makeCurrent()

        # Enable OpenGL features
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)  # Anti-aliasing
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Set the clear color
        gl.glClearColor(clear_color[0], clear_color[1], clear_color[2], 1.0)

    def render(self, scene: object, camera: object, clear_color: bool = True, clear_depth: bool = True, render_target: RenderTarget = None) -> None:
        """
        Render the scene using the specified camera.
        :param scene: The scene to render.
        :param camera: The camera to use for rendering.
        :param clear_color: Whether to clear the color buffer.
        :param clear_depth: Whether to clear the depth buffer.
        :param render_target: Optional render target for offscreen rendering.
        """
        # Ensure the OpenGL context is current
        if self.parent_widget:
            self.parent_widget.makeCurrent()

        # Filter descendants
        descendant_list = scene.descendant_list
        mesh_list = [x for x in descendant_list if isinstance(x, Mesh)]
        light_list = [x for x in descendant_list if isinstance(x, Light)]

        # Shadow pass
        if self.shadows_enabled:
            self._render_shadows(mesh_list)

        # Update camera
        camera.update_view_matrix()

        # Bind the appropriate framebuffer
        if render_target is None:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.parent_widget.defaultFramebufferObject() if self.parent_widget else 0)
            gl.glViewport(0, 0, self.window_size[0], self.window_size[1])
        else:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, render_target.frame_buffer)
            gl.glViewport(0, 0, render_target.width, render_target.height)

        # Clear buffers
        if clear_color:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        if clear_depth:
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)

        # Render meshes
        for mesh in mesh_list:
            if not mesh.visible:
                continue

            # Use the mesh's shader program
            gl.glUseProgram(mesh.material.program)

            # Bind the mesh's VAO
            gl.glBindVertexArray(mesh.vao_ref)

            # Update uniforms
            self._update_uniforms(mesh, camera, light_list)

            # Draw the mesh
            gl.glDrawArrays(mesh.material.settings["draw_mode"], 0, mesh.geometry.get_vertex_count())


    def _render_shadows(self, mesh_list):
        """
        Render shadow maps for the scene.
        :param mesh_list: List of meshes to render shadows for.
        """
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._shadow_object.render_target.frame_buffer)
        gl.glViewport(0, 0, self._shadow_object.render_target.width, self._shadow_object.render_target.height)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Use the shadow material
        gl.glUseProgram(self._shadow_object.material.program)
        self._shadow_object.update_internal()

        for mesh in mesh_list:
            if not mesh.visible or mesh.material.settings["draw_mode"] != gl.GL_TRIANGLES:
                continue

            gl.glBindVertexArray(mesh.vao_ref)
            self._shadow_object.material.uniforms["model_matrix"].data = mesh.global_matrix

            for var_name, uniform_obj in self._shadow_object.material.uniforms.items():
                uniform_obj.upload_data()

            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh.geometry.get_vertex_count())

    def _update_uniforms(self, mesh, camera, light_list):
        """
        Update the uniforms for a mesh.
        :param mesh: The mesh to update uniforms for.
        :param camera: The camera to use for view and projection matrices.
        :param light_list: List of lights in the scene.
        """
        # Update transformation matrices
        mesh.material.uniforms["model_matrix"].data = mesh.global_matrix
        mesh.material.uniforms["view_matrix"].data = camera.view_matrix
        mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix

        # Update light uniforms
        for i, light in enumerate(light_list):
            light_name = f"light_{i}"
            if light_name in mesh.material.uniforms:
                mesh.material.uniforms[light_name].data = light

        # Update camera position for specular lighting
        if "view_position" in mesh.material.uniforms:
            mesh.material.uniforms["view_position"].data = camera.global_position

        # Update shadow uniforms
        if self.shadows_enabled and "shadow_obj" in mesh.material.uniforms:
            mesh.material.uniforms["shadow_obj"].data = self._shadow_object

        # Upload all uniforms
        for uniform_obj in mesh.material.uniforms.values():
            uniform_obj.upload_data()

    def update_window_size(self, window_width, window_height):
        """
        Update the window size for the renderer.
        :param window_width: New window width.
        :param window_height: New window height.
        """
        self.window_size = (window_width, window_height)

    def enable_shadows(self, shadow_light: Light, strength: float = 0.5, resolution: list = [512, 512]):
        """
        Enable shadow rendering.
        :param shadow_light: The light source for shadows.
        :param strength: Shadow strength.
        :param resolution: Resolution of the shadow map.
        """
        self.shadows_enabled = True
        self._shadow_object = Shadow(light_source=shadow_light, resolution=resolution, strength=strength)
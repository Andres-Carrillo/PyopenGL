import OpenGL.GL as gl
from meshes.mesh import Mesh
from core.light.light import Light
from core.render_target import RenderTarget
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Renderer(object):
    def __init__(self,clear_color:list = [0.2, 0.2, 0.2],window_width:int=SCREEN_WIDTH,window_height:int = SCREEN_HEIGHT) -> None:
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

    def render(self,scene:object,camera:object,clear_color:bool = True,clear_depth:bool = True,render_target:RenderTarget=None) -> None:

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
    
        #update camera
        camera.update_view_matrix()

        kid_list = scene.get_children()

        viewable_filter = lambda x: isinstance(x,Mesh) and x.visible

        light_filter = lambda x: isinstance(x,Light)

        viewable_meshes = list(filter(viewable_filter,kid_list))

        light_list = list(filter(light_filter,kid_list))

        for mesh in viewable_meshes:
        
            # install the program for the mesh
            gl.glUseProgram(mesh.material.program)
            # bind vertex array object for the mesh
            gl.glBindVertexArray(mesh.vao_ref)

            # ================== update the uniforms for the mesh not stored in the material ==================
            #update the model matrix based on the mesh's world matrix
            mesh.material.uniforms["model_matrix"].data = mesh.get_world_matrix()

            # update the view matrix to match the camera
            mesh.material.uniforms["view_matrix"].data = camera.view_matrix

            # update the projection matrix to match the camera
            mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix

            # =========== Handle lights if any exist ==============
            # if the current mesh has a light material, update the light uniforms
            if "light_0" in mesh.material.uniforms.keys():
                number_of_lights = len(light_list) # number of lights in the scene
                for light_n in range(number_of_lights):
                    light_nmae = "light_" + str(light_n) # figure out the name of the light
                    light_inst = light_list[light_n] # get the light instance from the list

                    #update the light uniforms in the material incase the light has changed
                    mesh.material.uniforms[light_nmae].data = light_inst.get_light_data()


            # check if the mesh uses specular lighting
            if "view_position" in mesh.material.uniforms.keys():
                # update the view position to match the camera
                mesh.material.uniforms["view_position"].data = camera.global_position
# 

            # ================== update the uniforms for the mesh stored in the material ==================
            for var_name,uniform_obj in mesh.material.uniforms.items():
                uniform_obj.uploadData()


            #update the render settings for the material
            mesh.material.update_render_settings()

            # draw the mesh
            gl.glDrawArrays(mesh.material.settings["draw_mode"],0,mesh.geometry.get_vertex_count())


    def update_window_size(self,window_width, window_height):
            self.window_size = (window_width, window_height)
            
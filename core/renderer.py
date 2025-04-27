import OpenGL.GL as gl
from core.mesh import Mesh


class Renderer(object):
    def __init__(self,clear_color:list = [0,0,0]):
        gl.glEnable(gl.GL_DEPTH_TEST)
        # enables anti-aliasing
        gl.glEnable(gl.GL_MULTISAMPLE)


        gl.glClearColor(clear_color[0], clear_color[1], clear_color[2], 1.0)

    def render(self,scene:object,camera:object):
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
        #update camera
        camera.update_view_matrix()

        kid_list = scene.get_children()

        viewable_filter = lambda x: isinstance(x,Mesh) and x.visible

        viewable_meshes = list(filter(viewable_filter,kid_list))


        print('number of meshes to render:',len(viewable_meshes))
        i = 0
        for mesh in viewable_meshes:
            print("Rendering Mesh:", mesh, "Index:", i)
            i += 1
            
            gl.glViewport(0, 0, 800, 600)
            # Set default color to white, used when no objects present to cast shadows
            gl.glClearColor(1, 1, 1, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
            # Everything in the scene gets rendered with dept
            
            
            # install the program for the mesh
            gl.glUseProgram(mesh.material.program)
            # bind vertex array object for the mesh
            gl.glBindVertexArray(mesh.vao_ref)
            # gl.glDisable(gl.GL_CULL_FACE)

            # ================== update the uniforms for the mesh not stored in the material ==================
            #update the model matrix based on the mesh's world matrix
            mesh.material.uniforms["model_matrix"].data = mesh.get_world_matrix()

            # print(f"Model Matrix: {mesh.material.uniforms['model_matrix'].data}")

            # update the view matrix to match the camera
            mesh.material.uniforms["view_matrix"].data = camera.view_matrix

            # print(f"View Matrix: {mesh.material.uniforms['view_matrix'].data}")

            # update the projection matrix to match the camera
            mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix
# 
            # print(f"Projection Matrix: {mesh.material.uniforms['projection_matrix'].data}")

            # ================== update the uniforms for the mesh stored in the material ==================
            for var_name,uniform_obj in mesh.material.uniforms.items():
                uniform_obj.uploadData()


            #update the render settings for the material
            mesh.material.update_render_settings()

            # draw the mesh
            gl.glDrawArrays(mesh.material.settings["draw_mode"],0,mesh.geometry.get_vertex_count())

            print("Draw Mode:", mesh.material.settings["draw_mode"])

            # unbind the vertex array object
            # gl.glBindVertexArray(0)



            # for var_name,attrib_obj in mesh.geometry.attributes.items():
            #             print(f"Adding attribute {var_name} to the VAO")
            #             attrib_obj.associateVariable(mesh.material.program,var_name)
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from core.base import Base
from material.basic.surface import SurfaceMaterial
from geometry.simple3D.box import BoxGeometry
from meshes.mesh import Mesh
import OpenGL.GL as gl
from core.rendering.camera import Camera

class Test(Base):
    def __init__(self):
        super().__init__()
        self.geometry = BoxGeometry()
        self.material = SurfaceMaterial()
        self.mesh = Mesh(self.geometry, self.material)

        # Create a camera
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.set_position([0, 0, 4])  # Position the camera 4 units away from the origin
        self.camera.update_view_matrix()  # Update the view matrix based on the camera's position and orientation

    def update(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Install the program for the mesh
        gl.glUseProgram(self.mesh.material.program)

        # Bind vertex array object for the mesh
        gl.glBindVertexArray(self.mesh.vao_ref)

        # Update the model matrix
        self.mesh.material.uniforms["model_matrix"].data = self.mesh.global_matrix

        # Update the view and projection matrices
        self.mesh.material.uniforms["view_matrix"].data = self.camera.view_matrix
        self.mesh.material.uniforms["projection_matrix"].data = self.camera.projection_matrix

        # Upload all uniforms
        for var_name, uniform_obj in self.mesh.material.uniforms.items():
            uniform_obj.upload_data()

        # Update the render settings for the material
        self.mesh.material.update_render_settings()

        # Draw the mesh
        gl.glDrawArrays(self.mesh.material.settings["draw_mode"], 0, self.mesh.geometry.get_vertex_count())

if __name__ == "__main__":
    test = Test()
    test.run()
    test.quit()

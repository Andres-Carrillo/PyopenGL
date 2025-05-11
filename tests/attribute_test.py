import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from core.base import Base
from core.utils.openGLUtils import GlUtils
from core.glsl.attribute import Attribute
from core.utils.input import Input
import OpenGL.GL as gl
import glfw


class DrawHex(Base):
    def __init__(self):
        super().__init__()
        self._init_program()
       

    def _init_program(self) -> None:
        self._init_vertex_shader()
        self._init_fragment_shader()
        
        self.program_ref = GlUtils.InitializeProgram(self.vs_code, self.framgent_code)
        self.vao_ref = gl.glGenVertexArrays(1)

        gl.glBindVertexArray(self.vao_ref)
        gl.glLineWidth(14)
        gl.glPointSize(14)

        position_data = [
            [0.8, 0.0, 0.0],
            [0.4, 0.6, 0.0],
            [-0.4, 0.6, 0.0],
            [-0.8, 0.0, 0.0],
            [-0.4, -0.6, 0.0],
            [0.4, -0.6, 0.0]
        ]
        
        self.vertex_count = len(position_data)

        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        # Enable the vertex attribute array
        gl.glEnableVertexAttribArray(gl.glGetAttribLocation(self.program_ref, "position"))

    def update(self) -> None:      
            # Use the shader program
            gl.glUseProgram(self.program_ref)

            # Draw the hexagon
            gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, self.vertex_count)

 



    def _init_vertex_shader(self) -> None:
        self.vs_code = """
        in vec3 position;
        void main(){
            gl_Position = vec4(position.x, position.y, position.z, 1.0); // Draw point at location specified by position
        }
        """

    def _init_fragment_shader(self) -> None:
        self.framgent_code = """
        out vec4 frag_color;
        void main(){
            frag_color = vec4(1.0, 1.0, 0.0, 1.0); // color to be used
        }
        """

    def quit(self):
        gl.glDeleteProgram(self.program_ref)
        gl.glDeleteVertexArrays(1, [self.vao_ref]) 
        return super().quit()




class DrawMultipleObjects(Base):
    def __init__(self, title = "My App", major_version = 3, minor_version = 3):
        super().__init__(title, major_version, minor_version)
        self._init_program()


    def _init_program(self) -> None:
        self._init_vertex_shader()
        self._init_fragment_shader()

        self.program_ref = GlUtils.InitializeProgram(self.vs_code, self.fs_code)
    
        tri_position_data = [
            [-0.5, 0.8, 0.0],
            [-0.2, 0.2, 0.0],
            [-0.8, 0.2, 0.0]
        ]

        square_position_data = [
            [0.8,0.8,0.0],
            [0.8,0.2,0.0],
            [0.2,0.2,0.0],
            [0.2,0.8,0.0]
        ]
        
        self.vao_tri_ref = gl.glGenVertexArrays(1)
                # Bind the triangle VAO 
        gl.glBindVertexArray(self.vao_tri_ref)

     
        self.tri_vertex_count = len(tri_position_data)
        self.square_vertex_count = len(square_position_data)


        #set up the triangle vertex attribute
        tri_position_attribute = Attribute("vec3", tri_position_data)
        tri_position_attribute.associate_variable(self.program_ref, "position")
        gl.glBindVertexArray(0)  

        self.vao_square_ref = gl.glGenVertexArrays(1)

        # bind the square VAO
        gl.glBindVertexArray(self.vao_square_ref)
        
        #set up the square vertex attribute
        square_position_attribute = Attribute("vec3", square_position_data)
        square_position_attribute.associate_variable(self.program_ref, "position")

        gl.glBindVertexArray(0)  # Unbind the VAO

        # Enable the vertex attribute array
        gl.glEnableVertexAttribArray(gl.glGetAttribLocation(self.program_ref, "position"))




    def update(self):
        gl.glUseProgram(self.program_ref)

        #draw triangle 
        gl.glBindVertexArray(self.vao_tri_ref)
        gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.tri_vertex_count)

        #draw square
        # bind the square VAO
        gl.glBindVertexArray(self.vao_square_ref)
        gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.square_vertex_count)                    

    def _init_vertex_shader(self) -> None:
        self.vs_code = """
                           in vec3 position;
                           void main(){
                               gl_Position = vec4(position.x, position.y, position.z, 1.0); // Draw point at location specified by position
                           }
                        """

    def _init_fragment_shader(self) -> None:    
        self.fs_code = """
                           out vec4 frag_color;
                           void main(){
                               frag_color = vec4(1.0, 1.0, 0.0, 1.0); // color to be used
                           }
                        """

    # def update(self) -> None:
    #     pass

    def quit(self) -> None:
        gl.glDeleteProgram(self.program_ref)
        gl.glDeleteVertexArrays(1, [self.vao_square_ref, self.vao_tri_ref]) 
        return super().quit()



if __name__ == "__main__":
    my_app = DrawMultipleObjects()
    my_app.run()
    my_app.quit()
import glfw
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.utils.input import Input
from core.utils.timer import Timer
from core.utils.fps import FPS
import OpenGL.GL as gl
import pygame as pg
from core.rendering.scene import Scene
from core.rendering.renderer import Renderer
from tools.grid import GridTool
from core.rendering.camera import Camera
from tools.movement_rig import MovementRig
from math import pi
import imgui
from imgui.integrations.glfw import GlfwRenderer

""" 
        Base class for all glfw only applications.
        This class handles the initialization of GLFW,
        the creation of a window, and the main loop.
        It also provides a method for updating the application
        state and rendering the scene.
        Derived classes should implement the update method
        to provide their own application logic.
"""
class Base:
    """     
        Args:
            title (str): The title of the window.
            major_version (int): The major version of OpenGL to use.
            minor_version (int): The minor version of OpenGL to use.
    """
    def __init__(self, title:str = "My App", major_version:int = 3, minor_version:int =3) -> None:
        # Initialize pygame used for image loading and other utilities
        pg.init()

        # Initialize GLFW
        self._init_glfw(major_version, minor_version)
        
        # Create a windowed mode window and its OpenGL context
        self._init_window(title)

        # initialize class variables
        self._init_vars()
        
        # setup callbacks for window events
        self.input_handler.set_callbacks(self.window)

        # set resize callbacl for window
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)
        
        # set the background color
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)  

    """
        Initializes GLFW with the given OpenGL version.
        Args:
            major_version (int): The major version of OpenGL to use.
            minor_version (int): The minor version of OpenGL to use.
            Raises:
                Exception: If GLFW could not be initialized.
    """

    def _init_glfw(self,minor_version:int,major_version:int) -> None:
        # initialize GLFW and raise exception if it fails
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")

        # Set the window hints for OpenGL version
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    """
        Initializes the GLFW window with the given title.
        Args:
            title (str): The title of the window.
        Raises:
            Exception: If the GLFW window could not be created.
    """
    def _init_window(self, title:str) -> None:
        self.window_width = SCREEN_WIDTH
        self.window_height = SCREEN_HEIGHT

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(self.window_width,self.window_height, title, None, None)

        # set initial veiwport
        gl.glViewport(0, 0, self.window_width, self.window_height)
        
        # store title incase of FPS counter
        self.title = title
        
        # Check if the window was created successfully 
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)

        # Enable V-Sync
        glfw.swap_interval(1)
    
    """
            Initializes the variables used in the application.
            This function is called in the constructor.
            It is not necessary to call this function manually.
    """
    def _init_vars(self) -> None:
        #  core app variables
        self.timer = Timer()
        self.fps_counter = FPS() 
        self.show_fps = True
        self.input_handler = Input()


    """
        Derived classes should implement this function to update
        the application state, render the scene, and handle input.
    """
    def update(self):
        pass

    """
            Run function of an application.
            derived classes need not to implement this function.
            Unless they wish to extend this function and add their own logic.
    """
    def run(self) -> None:
        # main loop for all applications
        while not glfw.window_should_close(self.window):
            # update to be implemented in derived classes
            self.update()
           
            #swap buffers
            glfw.swap_buffers(self.window)

            # poll events
            self.input_handler.update()

            # check for quit
            if self.input_handler.quit:
                break
            
            # add FPS counter to the window title
            if self.show_fps:
                self._display_fps()

    """   
        Calculates the frames per second (FPS) and displays it in the window title. 
    """
    def _display_fps(self) -> None:
            glfw.set_window_title(self.window, self.title + f"- FPS: {self.fps_counter.update():.2f}")

    """
        Quits the application by destroying the window and terminating GLFW.
        It cleans up the resources used by the application.
        It is called automatically when the object is deleted.
        It is also called in the run method when the user quits the application.
        It is not necessary to call this method manually.
    """
    def quit(self) -> None:
        if self.window:
            glfw.destroy_window(self.window)
            self.window = None
        
        if glfw:
            glfw.terminate()
    
    """
        Destructor for the Base class.
        Cleans up the resources used by the application.
        It is called automatically when the object is deleted.
    """
    def __del__(self) -> None:
        self.quit()

    """
        Callback function for window resize events.
        This function is called when the window is resized.
        It adjusts the OpenGL viewport to match the new window size.
        Args:
            window: The GLFW window that was resized.
            width (int): The new width of the window.
            height (int): The new height of the window."""
    def _on_resize(self, window, width, height) -> None:
        gl.glViewport(0, 0, width, height)
        self.window_width = width
        self.window_height = height


from imgui.integrations.glfw import GlfwRenderer
class ImGuiBase:
    """
    Base class for all applications using ImGui and GLFW.
    This class handles the initialization of GLFW, ImGui, and the OpenGL context.
    Derived classes should implement the `update` and `render` methods to provide
    their own application logic and rendering.
    """

    def __init__(self, title: str = "My App", width: int = 800, height: int = 600,background_color:list=[0.1, 0.1, 0.1, 1.0],
                 show_fps:bool=True,major_version:int=3,minor_version:int=3,profile = glfw.OPENGL_CORE_PROFILE) -> None:
        
        self._init_glfw(title, width, height, major_version, minor_version, profile)

        self._init_imgui()


       
        # Store window properties
        self.title = title
        self.window_width = width
        self.window_height = height

        # Initialize utility classes
        self.timer = Timer()
        self.fps_counter = FPS()
        self.show_fps = show_fps
        self.input_handler = Input()
        self.imgui_renderer = GlfwRenderer(self.window)

        self.input_handler.set_callbacks(self.window,self.imgui_renderer)

        self._init_gl(background_color)

        # Set resize callback
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)



    def _init_glfw(self, title: str, width: int, height: int, major_version: int, minor_version: int, profile) -> None:
        # Initialize GLFW
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")

        # Set OpenGL version and profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(glfw.OPENGL_PROFILE, profile)

        # Create a GLFW window
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)

        # Enable V-Sync
        glfw.swap_interval(1)

    def _init_imgui(self) -> None:
         # Initialize ImGui
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        self.io = imgui.get_io()


    def _init_gl(self, background_color: list) -> None:
        # Set the OpenGL viewport
        gl.glViewport(0, 0, self.window_width, self.window_height)

        # Set the background color
        gl.glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])


    def _on_resize(self, window, width, height) -> None:
        """
        Callback function for window resize events.
        Adjusts the OpenGL viewport to match the new window size.
        """
        self.window_width = width
        self.window_height = height
        gl.glViewport(0, 0, width, height)

    def update(self):
        """
        Derived classes should implement this function to update
        the application state and handle input.
        """
        pass

    def render(self):
        """
        Derived classes should implement this function to render
        the scene using OpenGL.
        """
        pass

    def run(self) -> None:
        """
        Main loop for the application. Handles ImGui rendering,
        OpenGL rendering, and GLFW event polling.
        """
        while not glfw.window_should_close(self.window):
            # Poll events
            # glfw.poll_events()
            self.impl.process_inputs()
            self.input_handler.update()

             # Check for quit
            if self.input_handler.quit:
                break

            # Start a new ImGui frame
            imgui.new_frame()

            # Update application logic
            self.update()

            # Clear the screen
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            # Render the scene
            self.render()

            # Render ImGui
            imgui.render()
            self.impl.render(imgui.get_draw_data())

            # Swap buffers
            glfw.swap_buffers(self.window)

            
           

            # Display FPS in the window title
            if self.show_fps:
                self._display_fps()

        # Cleanup
        self.quit()

    def _display_fps(self) -> None:
        """
        Calculates the frames per second (FPS) and displays it in the window title.
        """
        fps = self.fps_counter.update()
        glfw.set_window_title(self.window, f"{self.title} - FPS: {fps:.2f}")

    def quit(self) -> None:
        """
        Cleans up resources and terminates GLFW and ImGui.
        """
        self.impl.shutdown()
        imgui.destroy_context()
        glfw.destroy_window(self.window)
        glfw.terminate()

    def __del__(self) -> None:
        """
        Destructor for the Base class. Ensures resources are cleaned up.
        """
        self.quit()




class BaseApp(ImGuiBase):
    def __init__(self, title="Test Framework", width=800, height=600,static_camera=True,display_grid=True):
        super().__init__(title, width, height)

        self.scene = Scene()
        self.renderer = Renderer()
        self.camera = Camera(aspect_ratio=width / height)

        if  static_camera:
             self.camera_rig = None
             self.camera.set_position([0, 1, 1])
        else:
            self.camera_rig = MovementRig()
            self.camera_rig.add(self.camera)
            self.add_to_scene(self.camera_rig)
            self.camera_rig.set_position([0.5, 1, 5])


        if display_grid:
            self.grid_tool = GridTool(size = self.camera.far,division=int(self.camera.far*2),grid_color=[1,1,1],center_color=[1,1,0])
            self.grid_tool.rotate_x(-pi/2)
            self.scene.add(self.grid_tool)
        else:
            self.grid_tool = None


    def update(self):
        # Example: Add ImGui UI elements
        imgui.begin("Example Window")
        imgui.text("Hello, ImGui!")
        if imgui.button("Click Me!"):
            print("Button clicked!")
        imgui.end()

    # for more complex applications, you can use the update method to handle input and update the scene
    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
        self._handle_input()
         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)
        #render the scene
        self.renderer.render(self.scene, self.camera)

    def _tick(self):
        self._time_delta = self.timer.delta_time()

    def _handle_input(self):
        if self.camera_rig is not None:
            self.camera_rig.update(self.input_handler, self._time_delta)


        

    def add_to_scene(self,mesh):
        self.scene.add(mesh)

import glfw
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.input import Input
from core.utils.timer import Timer
from core.utils.fps import FPS
import OpenGL.GL as gl
import pygame as pg
# import dearpygui.dearpygui as dpg
# import dearpygui.demo as demo

# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=600)

# demo.show_demo()

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()



""" 
        Base class for all applications.
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



# import dearpygui.dearpygui as dpg
# from core.utils.timer import Timer
# from core.utils.fps import FPS

# import dearpygui.dearpygui as dpg
# from core.utils.timer import Timer
# from core.utils.fps import FPS
# import OpenGL.GL as gl


# class DearGuiBase:
#     """
#     Base class for all applications using Dear PyGui with PyOpenGL rendering.
#     This class handles the initialization of Dear PyGui, the creation of a window,
#     and the integration of OpenGL rendering.
#     Derived classes should implement the `update` method to provide their own application logic.
#     """

#     def __init__(self, title: str = "My App", width: int = 800, height: int = 600) -> None:
#         # Initialize Dear PyGui context
#         dpg.create_context()

#         # Create a viewport (window)
#         self.title = title
#         self.window_width = width
#         self.window_height = height
#         dpg.create_viewport(title=self.title, width=self.window_width, height=self.window_height)

#         # Initialize class variables
#         self._init_vars()

#         # Set up Dear PyGui callbacks
#         self._setup_callbacks()

#         # Set up Dear PyGui viewport
#         dpg.setup_dearpygui()

#         # Initialize OpenGL
#         self._init_opengl()

#     def _init_vars(self) -> None:
#         """Initializes the variables used in the application."""
#         self.timer = Timer()
#         self.fps_counter = FPS()
#         self.show_fps = True

#     def _setup_callbacks(self) -> None:
#         """Sets up callbacks for Dear PyGui events."""
#         # Add a callback for window resize
#         dpg.set_viewport_resize_callback(self._on_resize)

#     def _init_opengl(self) -> None:
#         """Initializes OpenGL settings."""
#         # Set the OpenGL viewport to match the window size
#         gl.glViewport(0, 0, self.window_width, self.window_height)

#         # Set the background color
#         gl.glClearColor(0.1, 0.1, 0.1, 1.0)

#     def update(self):
#         """
#         Derived classes should implement this function to update
#         the application state, render the scene, and handle input.
#         """
#         pass

#     def render(self) -> None:
#         """
#         Handles OpenGL rendering. Derived classes can override this method
#         to implement custom rendering logic.
#         """
#         # Clear the screen
#         gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

#         # Example: Render a simple triangle (can be replaced with custom rendering logic)
#         gl.glBegin(gl.GL_TRIANGLES)
#         gl.glColor3f(1.0, 0.0, 0.0)  # Red
#         gl.glVertex2f(-0.5, -0.5)
#         gl.glColor3f(0.0, 1.0, 0.0)  # Green
#         gl.glVertex2f(0.5, -0.5)
#         gl.glColor3f(0.0, 0.0, 1.0)  # Blue
#         gl.glVertex2f(0.0, 0.5)
#         gl.glEnd()

#     def run(self) -> None:
#         """
#         Run function of the application.
#         Derived classes need not implement this function unless
#         they wish to extend it with additional logic.
#         """
#         # Show the viewport
#         dpg.show_viewport()

#         # Main loop for all applications
#         while dpg.is_dearpygui_running():
#             # Update logic to be implemented in derived classes
#             self.update()

#             # Perform OpenGL rendering
#             self.render()

#             # Add FPS counter to the window title
#             if self.show_fps:
#                 self._display_fps()

#             # Render Dear PyGui
#             dpg.render_dearpygui_frame()

#         # Cleanup after the main loop exits
#         self.quit()

#     def _display_fps(self) -> None:
#         """Calculates the frames per second (FPS) and displays it in the window title."""
#         fps = self.fps_counter.update()
#         dpg.set_viewport_title(f"{self.title} - FPS: {fps:.2f}")

#     def quit(self) -> None:
#         """
#         Quits the application by destroying the Dear PyGui context.
#         It cleans up the resources used by the application.
#         """
#         dpg.destroy_context()

#     def __del__(self) -> None:
#         """Destructor for the Base class. Cleans up resources."""
#         self.quit()

#     def _on_resize(self, sender, app_data) -> None:
#         """
#         Callback function for window resize events.
#         Adjusts the OpenGL viewport to match the new window size.
#         Args:
#             sender: The sender of the event.
#             app_data: The event data containing the new width and height.
#         """
#         if isinstance(app_data, tuple):
#             self.window_width, self.window_height = app_data[0], app_data[1]
#         elif isinstance(app_data, dict):
#             self.window_width, self.window_height = app_data['width'], app_data['height']
#         else:
#             raise TypeError(f"Unexpected type for app_data: {type(app_data)}")

#         # Update the OpenGL viewport
#         gl.glViewport(0, 0, self.window_width, self.window_height)


import imgui
from imgui.integrations.glfw import GlfwRenderer

class ImGuiBase:
    """
    Base class for all applications using ImGui and GLFW.
    This class handles the initialization of GLFW, ImGui, and the OpenGL context.
    Derived classes should implement the `update` and `render` methods to provide
    their own application logic and rendering.
    """

    def __init__(self, title: str = "My App", width: int = 800, height: int = 600) -> None:
        # Initialize GLFW
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")

        # Set OpenGL version and profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # Create a GLFW window
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)

        # Enable V-Sync
        glfw.swap_interval(1)

        # Initialize ImGui
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        # Store window properties
        self.title = title
        self.window_width = width
        self.window_height = height

        # Initialize utility classes
        self.timer = Timer()
        self.fps_counter = FPS()
        self.show_fps = True

        # Set the OpenGL viewport
        gl.glViewport(0, 0, self.window_width, self.window_height)

        # Set the background color
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        # Set resize callback
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)

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
            glfw.poll_events()
            self.impl.process_inputs()

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
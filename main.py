from apps.base import SceneEditor
        
# Run the application
if __name__ == "__main__":

    app = SceneEditor( width=1280, height=720,static_camera=False,generate_terrain__at_start=False)
    app.run()

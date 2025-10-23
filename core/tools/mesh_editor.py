from core.meshes.mesh import Mesh
import imgui
import math

def draw_material_settings(mesh):
    # display the mesh's current material settings and allow the user to edit them
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Settings")
    if open_header:
        for key, value in mesh.material.settings.items():
                if key == "wire_frame":
                    changed, new_value = imgui.checkbox("Wire Frame", value)
                    imgui.same_line()
                    if changed:
                        mesh.material.settings[key] = new_value
                if mesh.material.settings.get('wire_frame', False) and key == "line_width":
                    changed, new_value = imgui.slider_float("Line Width", value, 0.1, 10.0)
                    if changed:
                        mesh.material.settings[key] = new_value
                if key == "double_sided":
                    changed, new_value = imgui.checkbox("Double Sided", value)
                    imgui.same_line()
                    if changed:
                        mesh.material.settings[key] = new_value

def draw_position_editor(mesh):
     # Display the mesh's current position and allow the user to edit it
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Position transform")
    if open_header:
        changed_x, new_x_pos = imgui.input_int("X Position##pos", mesh.global_position[0])
        changed_y, new_y_pos = imgui.input_int("Y Position##pos", mesh.global_position[1])
        changed_z, new_z_pos = imgui.input_int("Z Position##pos", mesh.global_position[2])
        if changed_x or changed_y or changed_z:
            mesh.set_position([new_x_pos, new_y_pos, new_z_pos])

def draw_rotation_editor(mesh,range =(-math.pi, math.pi)):
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Rotation transform")
    if open_header:
        x_rot_changed, new_x_rot = imgui.slider_float("X Rotation", mesh.ueler_angles[0], range[0], range[1])
        y_rot_changed, new_y_rot = imgui.slider_float("Y Rotation", mesh.ueler_angles[1], range[0], range[1])
        z_rot_changed, new_z_rot = imgui.slider_float("Z Rotation", mesh.ueler_angles[2], range[0], range[1])
        if x_rot_changed or y_rot_changed or z_rot_changed:
            mesh.set_euler_rotation([new_x_rot*360, new_y_rot*360, new_z_rot*360])


class MeshEditorModel:
    def __init__(self, mesh: Mesh = None):
        self.mesh = mesh
        self.position = mesh.global_position if mesh else [0, 0, 0]
        self.rotation = mesh.ueler_angles if mesh else [0, 0, 0]
        self.scale = mesh.scale if mesh else [1, 1, 1]
        self.editing_shader = False


class MeshEditorView:
    def __init__(self, model:MeshEditorModel):
        self.model = model


    def render(self):
        imgui.text("{}".format(self.model.mesh.geometry.object_type))


        # Display the mesh's current position and allow the user to edit it
        draw_position_editor(self.model.mesh)

        # Display the mesh's current rotation and allow the user to edit it
        draw_rotation_editor(self.model.mesh)

        draw_material_settings(self.model.mesh)

        imgui.separator()



class MeshEditorController:
    def __init__(self, view:MeshEditorView):
        self.model = view.model
        self.view = view

    def render(self):
        if self.model.mesh is not None:
     
            self.view.render()

    def change_mesh(self, mesh: Mesh = None):

        self.model.mesh = mesh

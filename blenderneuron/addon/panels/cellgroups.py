import bpy, random
from blenderneuron.addon.panels import BlenderNEURONPanel

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       FloatProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)


class CUSTOM_UL_CellListWidget(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "selected", text="")
        layout.label(item.name)

    def invoke(self, context, event):
        pass


class CUSTOM_UL_CellGroupListWidget(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "selected", text="")
        layout.prop(item, "name", text="", emboss=False)

    def invoke(self, context, event):
        pass


class CUSTOM_PT_NEURON_CellGroups(BlenderNEURONPanel, Panel):
    bl_idname = 'CUSTOM_PT_NEURON_CellGroups'
    bl_label = "Cell Groups"

    @classmethod
    def poll(cls, context):
        """
        Checks if a connection to NEURON has been established
        """
        return hasattr(bpy.types.Object, "BlenderNEURON_node") and \
               bpy.types.Object.BlenderNEURON_node is not None and \
               bpy.types.Object.BlenderNEURON_node.client is not None

    def draw(self, context):
        scene = context.scene

        row = self.layout.row()

        row.template_list("CUSTOM_UL_CellGroupListWidget", "", \
                          scene, "BlenderNEURON_neuron_cellgroups", \
                          scene, "BlenderNEURON_neuron_cellgroups_index", \
                          rows=3)

        col = row.column(align=True)
        col.operator("custom.cell_group_add", icon='ZOOMIN', text="")
        col.operator("custom.cell_group_remove", icon='ZOOMOUT', text="")


class CUSTOM_PT_NEURON_GroupCells(BlenderNEURONPanel, Panel):
    bl_idname = 'CUSTOM_PT_NEURON_GroupCells'
    bl_label = "Cells in Group"

    @classmethod
    def poll(cls, context):
        return BlenderNEURONPanel.groups_exist(context)

    def draw(self, context):
        group = self.get_group(context)

        self.layout.operator("custom.get_cell_list_from_neuron", text="Refresh NEURON Cell List", icon="FILE_REFRESH")

        self.layout.template_list("CUSTOM_UL_CellListWidget", "", \
                                  group, "cells", \
                                  group, "cells_index", \
                                  rows=5)

        col = self.layout.split(0.33)
        col.operator("custom.select_all_neuron_cells")
        col.operator("custom.select_none_neuron_cells")
        col.operator("custom.select_invert_neuron_cells")


class CUSTOM_PT_NEURON_GroupSettings(BlenderNEURONPanel, Panel):
    bl_idname = 'CUSTOM_PT_NEURON_GroupSettings'
    bl_label = "Cell Group Options"

    @classmethod
    def poll(cls, context):
        return BlenderNEURONPanel.groups_exist(context)

    def draw(self, context):

        group = self.get_group(context)

        col = self.layout
        col.prop(group, "recording_granularity", text="Record")
        col.prop(group, "record_variable", text="Variable")
        col.prop(group, "interaction_granularity", text="Interact")
        col.separator()

        row = col.split(0.5)
        row.prop(group, "import_activity", text="Import Activity")
        row.prop(group, "import_synapses", text="Import Synapses")


class CUSTOM_PT_NEURON_Import(BlenderNEURONPanel, Panel):
    bl_idname = 'CUSTOM_PT_NEURON_Import'
    bl_label = "Import"

    @classmethod
    def poll(cls, context):
        return BlenderNEURONPanel.groups_exist(context)

    def draw(self, context):
        scene = context.scene

        self.layout.operator("custom.import_selected_groups", text="Show Selected Cell Groups in Blender",
                             icon="PLAY")


class CUSTOM_PT_NEURON_SimulationSettings(BlenderNEURONPanel, Panel):
    bl_idname = 'CUSTOM_PT_NEURON_SimulationSettings'
    bl_label = "Simulation"

    @classmethod
    def poll(cls, context):
        """
        Checks if a connection to NEURON has been established
        """
        return hasattr(bpy.types.Object, "BlenderNEURON_node") and \
               bpy.types.Object.BlenderNEURON_node is not None and \
               bpy.types.Object.BlenderNEURON_node.client is not None

    def draw(self, context):
        settings = self.get_sim_settings(context)

        col = self.layout

        col.prop(settings, "neuron_tstop", text="Stop Time")
        col.prop(settings, "temperature", text="Temperature")

        col.operator("custom.import_selected_groups", text="Open Voltage Plot", icon="FCURVE")
        col.prop(settings, "integration_method")

        if settings.integration_method == 0:
            col.prop(settings, "time_step")

        if settings.integration_method == 1:
            col.prop(settings, "abs_tolerance")

        col.operator("custom.import_selected_groups", text="Init & Run", icon="POSE_DATA")

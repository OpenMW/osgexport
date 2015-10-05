# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
from bpy_extras.anim_utils import bake_action


# take care of restoring selection after
def bakeAnimation(scene, blender_object):
    frame_range = (scene.frame_start, scene.frame_end, scene.frame_step)
    # baking will replace the current action but we want to keep scene unchanged
    if blender_object.animation_data and blender_object.animation_data.action:
        original_action = blender_object.animation_data.action

    # Baking is done on the active object
    active_object_backup = scene.objects.active
    scene.objects.active = blender_object
    baked_action = bake_action(scene.frame_start,
                               scene.frame_end,
                               scene.frame_step,
                               do_clean=True,  # clean keyframes
                               do_constraint_clear=False,  # remove constraints from object
                               do_parents_clear=False,  # don't unparent object
                               do_object=True,  # bake solid animation
                               # visual keying bakes in worldspace, but here we want it local since we keep parenting
                               do_visual_keying=False)

    # restore original action
    if original_action:
        blender_object.animation_data.action = original_action

    scene.objects.active = active_object_backup

    return baked_action

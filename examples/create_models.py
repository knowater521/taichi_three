import taichi as ti
import taichi_three as t3
import numpy as np

ti.init(ti.cpu)

scene = t3.Scene()
mesh = t3.MeshGen()
mesh.quad([0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0])
model = t3.Model(mesh)
scene.add_model(model)

scene.set_light_dir([0.4, -1.5, -1.8])
gui = ti.GUI('Creating models', scene.res)
while gui.running:
    gui.running = not gui.get_event(ti.GUI.ESCAPE)
    model.L2W.offset[None] = [-0.5, -0.5, 0]
    scene.camera.from_mouse(gui)
    scene.render()
    gui.set_image(scene.img)
    gui.show()


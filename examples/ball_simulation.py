import taichi as ti
import taichi_glsl as ts
import taichi_three as t3
ti.init(ti.opengl)

N = 12
dt = 0.01

scene = t3.Scene()
model = t3.ScatterModel(radius=5)
scene.add_model(model)
camera = t3.Camera()
scene.add_camera(camera)
#camera.type = camera.ORTHO

pos = ti.Vector.field(3, ti.f32, N)
vel = ti.Vector.field(3, ti.f32, N)
radius = ti.field(ti.f32, N)

model.particles = pos


@ti.kernel
def init():
    for i in pos:
        pos[i] = ts.randNDRange(ts.vec3(-1), ts.vec3(1))
        vel[i] = ts.randNDRange(ts.vec3(-1.1), ts.vec3(1.1))
        radius[i] = ts.randRange(0.1, 0.2)

@ti.func
def interact(i, j):
    disp = pos[i] - pos[j]
    disv = vel[i] - vel[j]
    if disp.norm_sqr() < (radius[i] + radius[j]) ** 2 and disp.dot(disv) < 0:
        mass_i = radius[i] ** 3
        mass_j = radius[j] ** 3
        disp = ts.normalize(disp)
        vel[i], vel[j] = ts.momentumExchange(
                vel[i], vel[j], disp, mass_i, mass_j, 0.8)

@ti.kernel
def substep():
    for i in pos:
        acc = ts.vec(0, -1, 0)
        vel[i] += acc * dt

    for i in pos:
        for j in range(N):
            if i != j:
                interact(i, j)

    for i in pos:
        for j in ti.static(range(3)):
            if vel[i][j] < 0 and pos[i][j] < -1 + radius[i]:
                vel[i][j] *= -0.8
            if vel[i][j] > 0 and pos[i][j] > 1 - radius[i]:
                vel[i][j] *= -0.8

    for i in pos:
        pos[i] += vel[i] * dt

init()
gui = ti.GUI('Balls', camera.res)
while gui.running:
    gui.get_event(None)
    gui.running = not gui.is_pressed(ti.GUI.ESCAPE)
    for i in range(4):
        substep()
    camera.from_mouse(gui)
    scene.render()
    gui.set_image(camera.img)
    gui.show()

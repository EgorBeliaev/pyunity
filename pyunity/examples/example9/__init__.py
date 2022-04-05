from pyunity import Behaviour, ShowInInspector, RectTransform, Screen, Vector2, Input, CheckBox, Text, SceneManager, GameObject, Canvas, Texture2D, Gui, RectOffset, Logger, Image2D, FontLoader, RGB, Camera, Vector3, RenderTarget, MeshRenderer, Mesh, Material
import os

class Mover2D(Behaviour):
    rectTransform = ShowInInspector(RectTransform)
    speed = ShowInInspector(float, 300)
    def Start(self):
        self.rectTransform.offset.Move(Screen.size / 2)

    def Update(self, dt):
        movement = Vector2(Input.GetAxis("Horizontal"), -
                           Input.GetAxis("Vertical"))
        self.rectTransform.offset.Move(movement * dt * self.speed)
        self.rectTransform.rotation += 270 * dt

class FPSTracker(Behaviour):
    text = ShowInInspector(Text)
    def Start(self):
        self.a = 0
        self.t = []

    def Update(self, dt):
        self.t.append(dt)
        if len(self.t) > 200:
            self.t.pop(0)

        self.a += dt
        if self.a > 0.1:
            self.text.text = str(1 / (sum(self.t) / len(self.t)))
            self.a = 0

class CheckboxTracker(Behaviour):
    check = ShowInInspector(CheckBox)
    text = ShowInInspector(Text)
    def Update(self, dt):
        self.text.text = "On" if self.check.checked else "Off"

def main():
    scene = SceneManager.AddScene("Scene")
    canvas = GameObject("Canvas")
    canvas.AddComponent(Canvas)
    scene.Add(canvas)

    imgObject = GameObject("Image", canvas)
    rectTransform = imgObject.AddComponent(RectTransform)
    rectTransform.offset = RectOffset.Rectangle(100)
    imgObject.AddComponent(Mover2D).rectTransform = rectTransform

    img = imgObject.AddComponent(Image2D)
    img.depth = -0.1
    img.texture = Texture2D(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "example8", "logo.png"))
    scene.Add(imgObject)

    rect, button, text = Gui.MakeButton(
        "Button", scene, "Click me", FontLoader.LoadFont("Consolas", 20))
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(40, 25), Vector2(190, 50))
    button.callback = lambda: Logger.Log("Clicked")

    rect, checkbox = Gui.MakeCheckBox("Checkbox", scene)
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(300, 50), Vector2(325, 75))

    label = GameObject("Label")
    text = label.AddComponent(Text)
    text.text = "Off"
    text.color = RGB(0, 0, 0)
    label.AddComponent(RectTransform).offset = RectOffset(
        Vector2(330, 50), Vector2(425, 75))
    label.transform.ReparentTo(canvas.transform)
    scene.Add(label)
    tracker = rect.AddComponent(CheckboxTracker)
    tracker.text = text
    tracker.check = checkbox

    t = GameObject("Text", canvas)
    rect = t.AddComponent(RectTransform)
    rect.anchors.SetPoint(Vector2(1, 0))
    rect.offset.min = Vector2(-150, 25)
    text = t.AddComponent(Text)
    text.text = "60"
    text.color = RGB(0, 0, 0)
    t.AddComponent(FPSTracker).text = text
    scene.Add(t)

    cam = GameObject("Camera")
    camera = cam.AddComponent(Camera)
    camera.shadows = False
    cam.transform.eulerAngles = Vector3(0, 180, 0)
    scene.Add(cam)

    target = GameObject("Target", canvas)
    rect = target.AddComponent(RectTransform)
    rect.anchors.SetPoint(Vector2(1, 1))
    rect.offset.min = Vector2(-320, -200)
    target.AddComponent(RenderTarget).source = camera
    scene.Add(target)

    cube = GameObject("Cube")
    cube.transform.position = Vector3(0, 0, -10)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    scene.Add(cube)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()

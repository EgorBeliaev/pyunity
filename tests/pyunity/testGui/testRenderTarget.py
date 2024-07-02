import pytest
import OpenGL.GL as gl
from unittest.mock import Mock, patch
from pyunity.values import Vector2
from pyunity.gui import RenderTarget, Camera, RectTransform, PyUnityException, RectData, RectOffset
from PIL import Image
from unittest import mock

class TestRenderTarget:

    @pytest.fixture
    def setup_render_target(self):
        render_target = RenderTarget()
        render_target.gameObject = Mock()
        render_target.gameObject.scene = Mock()
        render_target.gameObject.scene.mainCamera = Mock()
        render_target.gameObject.scene.mainCamera.renderPass = False
        render_target.gameObject.scene.mainCamera.guiShader = Mock()
        render_target.gameObject.scene.mainCamera.guiShader.uniforms = {"projection": Mock()}

        rect_transform_mock = Mock(spec=RectTransform)
        rect_transform_mock.offset = RectOffset(Vector2(0, 0), Vector2(0, 0))

        rect_data = RectData(Vector2(0, 0), Vector2(800, 600))
        rect_transform_mock.GetRect.return_value = rect_data

        render_target.GetComponent = Mock(return_value=rect_transform_mock)
        render_target.framebuffer = 1  # Setting the framebuffer attribute
        render_target.size = Vector2(800, 600)  # Setting the size attribute
        return render_target

    def test_pre_render_sets_up_framebuffers(self, setup_render_target):
        render_target = setup_render_target
        render_target.source = Mock(spec=Camera)
        render_target.source.Resize = Mock()
        render_target.source.RenderDepth = Mock()
        render_target.source.RenderScene = Mock()
        render_target.source.RenderSkybox = Mock()
        render_target.source.Render2D = Mock()
        render_target.source.guiShader = Mock()
        render_target.source.guiShader.uniforms = {"projection": Mock()}
        render_target.genBuffers = Mock()
        render_target.setSize = Mock()

        render_target.PreRender()

        render_target.genBuffers.assert_called_once()
        render_target.source.Resize.assert_called_once_with(800, 600)
        render_target.source.RenderDepth.assert_called_once()
        render_target.source.RenderScene.assert_called_once()
        render_target.source.RenderSkybox.assert_called_once()

    def test_pre_render_raises_exception_for_main_camera(self, setup_render_target):
        render_target = setup_render_target
        render_target.source = render_target.gameObject.scene.mainCamera

        render_target.genBuffers = Mock()  # Mock genBuffers to avoid actual framebuffer setup

        with patch.object(render_target.source, 'renderPass', False):
            render_target.source.renderPass = True  # Ensure this is set to True to trigger the exception
            with pytest.raises(PyUnityException, match="Cannot render main camera with main camera"):
                render_target.PreRender()

    @patch("PIL.Image.frombytes")
    def test_save_img_creates_image_file(self, mock_frombytes, setup_render_target):
        render_target = setup_render_target
        render_target.framebuffer = 1
        render_target.size = Vector2(800, 600)
        mock_image = Mock()
        mock_frombytes.return_value = mock_image

        with patch.object(mock_image, 'transpose', return_value=mock_image) as mock_transpose:
            mock_image.save = Mock()

            render_target.saveImg("test_path.png")

            mock_frombytes.assert_called_once_with("RGB", (800, 600), mock.ANY)
            mock_transpose.assert_called_once_with(Image.Transpose.FLIP_TOP_BOTTOM)
            mock_image.save.assert_called_once_with("test_path.png")

    def test_gen_buffers_generates_framebuffers_textures_and_renderbuffers(self, setup_render_target):
        render_target = setup_render_target

        with patch("pyunity.gui.gl.glGenFramebuffers", return_value=1) as mock_gen_framebuffers, \
             patch("pyunity.gui.gl.glGenTextures", return_value=2) as mock_gen_textures, \
             patch("pyunity.gui.gl.glGenRenderbuffers", return_value=3) as mock_gen_renderbuffers, \
             patch("pyunity.gui.gl.glCheckFramebufferStatus", return_value=gl.GL_FRAMEBUFFER_COMPLETE):

            render_target.genBuffers(force=True)

            mock_gen_framebuffers.assert_called_once()
            mock_gen_textures.assert_called_once()
            mock_gen_renderbuffers.assert_called_once()

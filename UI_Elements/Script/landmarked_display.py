from godot import exposed, export, TextureRect, PoolByteArray, Image, ImageTexture

@exposed
class landmarked_display(TextureRect):

    shouldRun = export(bool, default = False)
    data = export(PoolByteArray, default = PoolByteArray([0]))

    def _reday(self):
        self.data = self.texture.get_data().get_data()
    
    def _process(self, delta):
        if self.shouldRun:
            self.texture = render_frames(self.data)

def render_frames(frame_data):
    image = Image()
    image.load_jpg_from_buffer(frame_data)
    image_texture = ImageTexture()
    image_texture.create_from_image(image)
    return image_texture 
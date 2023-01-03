from datetime import datetime
from typing import Optional

from PIL import Image
from pyzbar.pyzbar import decode, Decoded

Image.MAX_IMAGE_PIXELS = 615040000

WHITE: int = 255


class QrDecoder:
    def __init__(self, im: Image, wrong_qr: Image, qr_dimension: int = 25, border_width: int = 3):
        self._image: Image = im.convert(mode="1")
        self._wrong_qr: Image = wrong_qr.convert("1")
        self._qr_dimension = qr_dimension
        self._border_width = border_width

    def decode_image(self) -> Optional[str]:
        main = self._cut_image()
        main_thumb: Image = main.copy()
        main_thumb.thumbnail((self._qr_dimension * 10, self._qr_dimension * 10))
        main_thumb.save(f"out/dec16-qr-main.png")

        quarter_decoder = QuarterDecoder(wrong_qr=self._wrong_qr, qr_dimension=self._qr_dimension)
        (w, h) = main.size
        for i in list(range(self._qr_dimension)):
            for j in list(range(self._qr_dimension)):
                left = i * w / self._qr_dimension
                upper = j * h / self._qr_dimension
                right = (i + 1) * w / self._qr_dimension
                lower = (j + 1) * h / self._qr_dimension
                file = quarter_decoder.decode(main.crop((left, upper, right, lower)))
                if file:
                    return file
        return None

    def _cut_image(self) -> Image:
        (width_px, height_px) = self._image.size
        unit_width_px = width_px / (self._qr_dimension + 2 * self._border_width)
        border_width_px = self._border_width * unit_width_px
        left, upper = border_width_px, border_width_px
        qr_dimension_px = self._qr_dimension * border_width_px / self._border_width
        right, lower = qr_dimension_px + border_width_px, qr_dimension_px + border_width_px
        return self._image.crop((left, upper, right, lower))


class QuarterDecoder:

    def __init__(self, wrong_qr: Image, qr_dimension: int):
        assert wrong_qr.mode == "1"
        if wrong_qr.size != (qr_dimension, qr_dimension):
            wrong_qr = wrong_qr.copy()
            wrong_qr.thumbnail((qr_dimension, qr_dimension))
        self._wrong_qr = wrong_qr
        self._wrong_qr_white_sum = sum(wrong_qr.getdata())
        self._dimension = qr_dimension
        self._target_data = self._get_target_data()
        self._counter = 0

    def _get_target_data(self) -> Image:
        data = [0, 0, 0, 0, 0, 0, 0, 1,
                0, 1, 1, 1, 1, 1, 0, 1,
                0, 1, 0, 0, 0, 1, 0, 1,
                0, 1, 0, 0, 0, 1, 0, 1,
                0, 1, 0, 0, 0, 1, 0, 1,
                0, 1, 1, 1, 1, 1, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 1,
                1, 1, 1, 1, 1, 1, 1, 1, ]
        return [v * WHITE for v in data]

    def decode(self, im: Image) -> Optional[str]:
        assert im.mode == "1"

        thumb = im.copy()
        thumb.thumbnail((self._dimension, self._dimension))

        if self._has_qr_targets(thumb):
            self._counter += 1
            if self._counter % 200 == 0:
                print(f"Found {self._counter} QR codes.")
            if not self._is_wrong_qr_code(thumb):
                # Decode
                name = f"out/dec16-qr-flag-{int(datetime.now().timestamp())}.png"
                thumb.save(name)
                print(f"Saved {name}")
                return name
        elif not self._is_white(im):
            # Subdivide into 4 quarters and evaluate these
            (w, h) = im.size
            if w <= self._dimension:
                # print(f"Cannot subdivide any further ({w}x{h}).")
                return None
            for i in range(2):
                for j in range(2):
                    # Decode a sub-QR
                    file = self.decode(im.crop((i * w / 2, j * h / 2, (i + 1) * w / 2, (j + 1) * h / 2)))
                    if file:
                        return file
        return None

    def _has_qr_targets(self, im: Image) -> bool:
        target_region = (0, 0, 8, 8)

        return list(im.crop(target_region).getdata()) == self._target_data \
            or list(im.rotate(180).crop(target_region).getdata()) == self._target_data

    def _is_white(self, im: Image) -> bool:
        (width, height) = im.size
        return sum(im.getdata()) == width * height * WHITE

    def _is_wrong_qr_code(self, im: Image) -> bool:
        # return (self._is_wrong_qr_code_v1(im)
        #         or self._is_wrong_qr_code_v1(im.transpose(Transpose.FLIP_LEFT_RIGHT)))
        return self._is_wrong_qr_code_v2(im)

    def _is_wrong_qr_code_v1(self, im: Image) -> bool:
        r0 = list(im.getdata())
        r90 = list(im.rotate(90).getdata())
        r180 = list(im.rotate(180).getdata())
        r270 = list(im.rotate(270).getdata())
        wrong_im_data = list(self._wrong_qr.getdata())
        return r0 == wrong_im_data or r90 == wrong_im_data or r180 == wrong_im_data or r270 == wrong_im_data

    def _is_wrong_qr_code_v2(self, im: Image) -> bool:
        return self._wrong_qr_white_sum == sum(im.getdata())


def main():
    start = datetime.now()
    im = Image.open("haystack_monochrome.png")
    wrong_qr = Image.open("wrong_qr_monochrome.png")
    decoder = QrDecoder(im, wrong_qr)
    file = decoder.decode_image()
    if file:
        wbg = Image.new(mode="1", size=(27, 27), color=WHITE)
        wbg.paste(Image.open(file), (1, 1))
        d = decode(wbg)
        if len(d) > 0:
            decoded: Decoded = d[0]
            print(decoded.data.decode()[:5])
    print(f"Duration: {datetime.now() - start}")


if __name__ == '__main__':
    main()

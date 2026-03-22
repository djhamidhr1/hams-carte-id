import barcode
from barcode.writer import ImageWriter
from PyQt5.QtGui import QPixmap, QImage
import io

def generate_barcode(data="123456789012", fmt="code128"):
    try:
        writer = ImageWriter()
        writer.set_options({
            "module_width": 0.8,
            "module_height": 8.0,
            "font_size": 6,
            "text_distance": 1.5,
            "quiet_zone": 1.0,
        })
        bc_class = barcode.get_barcode_class(fmt)
        bc = bc_class(data, writer=writer)
        buf = io.BytesIO()
        bc.write(buf)
        buf.seek(0)
        qimg = QImage.fromData(buf.read())
        return QPixmap.fromImage(qimg)
    except Exception as e:
        print(f"Erreur barcode: {e}")
        return None
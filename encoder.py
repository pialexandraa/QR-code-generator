import segno # for SVG generation
from io import BytesIO
from qrcode import ERROR_CORRECT_M, constants, QRCode

# Function to generate PNG bytes of a QR code from input data:
def qrcode_png_bytes(
        data: str,
        *,
        #version: int = 1,
        error_correction: str = "M",
        box_size: int = 10,
        border: int = 4,
        fill_color: str = "#000000",
        back_color: str = "#ffffff",
        scale: int = None
) -> BytesIO:
    # map error correction level in dict, to qrcode.constants
    error_correction_map = {
        "L": constants.ERROR_CORRECT_L, # 7% error correction, low
        "M": constants.ERROR_CORRECT_M, # 15% error correction, medium/default
        "Q": constants.ERROR_CORRECT_Q, # 25% error correction, quartile
        "H": constants.ERROR_CORRECT_H, # 30% error correction, high
    }

    error_correction_level = error_correction_map.get(error_correction.upper(), ERROR_CORRECT_M)

    qrcode = QRCode(
        box_size=box_size,
        border=border,
        error_correction=error_correction_level,
        #version=version,
    )
    qrcode.add_data(data)
    qrcode.make(fit=True)
    image = qrcode.make_image(fill_color=fill_color, back_color=back_color)
    
    # in memory bytes buffer
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf

# Function to generate SVG bytes of a QR code from input data:
def qrcode_svg_bytes(
        data: str,
        *,
        #version: int = 1,
        border: int = 4,
        dark: str ="#000000",
        light: str = "#ffffff",
        scale: int = None,
        error_correction: str = "M"
        ) -> str:
    # Minimal error handling; additional error checking done in segno:
    '''
    if version is not None and (version <= 0 or version > 40):
        raise ValueError("The version must be between 1 and 40, in order to have a QR matrix.")
    '''
    if border < 0:
        raise ValueError("The border must be a non-negative integer.")
    if error_correction.upper() not in {"L", "M", "Q", "H"}:
        raise ValueError("The error correction must follow the standard levels: L, M, Q or H.")

    # Return SVG text for QR content using segno (vector):
    qrcode = segno.make(data, error=error_correction.upper()) #version=version
    buf = BytesIO()
    # 'scale' controls SVG output size; omit if None for automatic sizing.
    save_kwargs = {"kind": "svg", "border": border, "dark": dark, "light": light}
    if scale is not None:
        save_kwargs["scale"] = scale
    qrcode.save(buf, **save_kwargs)
    svg_text = buf.getvalue().decode()
    return svg_text
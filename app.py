from flask import (Flask, request, render_template, make_response, abort)
from encoder import qrcode_png_bytes, qrcode_svg_bytes
from io import BytesIO

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/qrcode.png")
def qrcode_png():
    data = (request.args.get("data") or "").strip()
    if not data:
        abort(400, "Data is missing")
        return None
    box = int(request.args.get("box", 10))
    border = int(request.args.get("border", 4))
    fill = request.args.get("fill", "#000000")
    back = request.args.get("back", "#ffffff")
    error_correction = (request.args.get("error_correction", "M") or "M").upper()

    if error_correction not in {"L", "M", "Q", "H"}:
        abort(400, "Invalid error_correction (use L, M, Q, or H)")
        return None
    elif box <= 0:
        abort(400, "Box size must be positive")
        return None
    elif border < 0:
        abort(400, "Border must be non-negative")
        return None

    png_buf = qrcode_png_bytes(
        data,
        box_size=box,
        border=border,
        fill_color=fill,
        back_color=back,
        error_correction=error_correction,
    )
    response = make_response(png_buf.getvalue())
    response.headers.set("Content-Type", "image/png")
    response.headers.set("Content-Disposition", "inline; filename=qrcode.png")
    return response

@app.get("/qrcode.svg")
def qrcode_svg():
    data = (request.args.get("data") or "").strip()
    if not data:
        abort(400, "Data is missing")
        return

    border = int(request.args.get("border", 4))
    # Read SVG-specific parameters
    scale_param = request.args.get("scale")
    scale = int(scale_param) if scale_param is not None else None
    dark = request.args.get("dark", "#000000")
    light = request.args.get("light", "#ffffff")
    error_correction = (request.args.get("error_correction", "M") or "M").upper()

    if error_correction not in {"L", "M", "Q", "H"}:
        abort(400, "Invalid error_correction (use L, M, Q, or H)")
        return
    if border < 0:
        abort(400, "Border must be non-negative")
        return
    if scale is not None and scale <= 0:
        abort(400, "Scale must be a positive integer")
        return

    svg_text = qrcode_svg_bytes(
        data,
        border=border,
        dark=dark,
        light=light,
        scale=scale,
        error_correction=error_correction,
    )
    response = make_response(svg_text)
    response.headers.set("Content-Type", "image/svg+xml; charset=utf-8")
    response.headers.set("Content-Disposition", "inline; filename=qrcode.svg")
    return response


if __name__ == "__main__":
    app.run(debug=True)
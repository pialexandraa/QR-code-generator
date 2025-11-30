// Grab references to key DOM elements (1-time operation avoiding repeated lookups)
const img = document.getElementById("img");
const svgImg = document.getElementById("svgimg");
const form = document.getElementById("f"); // HTML form has id="f"
const dlBtnPNG = document.getElementById("download-png");
const dlBtnSVG = document.getElementById("download-svg");

// Function to handle form submissions for PNG and SVG generation
//async function handleFormSubmit(event, isSVG) {
    //event.preventDefaul   t(); // Prevent default form submission behavior
//}
// Helper: build qrcode.png or qrcode.svg URL with curent form values:
function pngUrl() {
    const params = new URLSearchParams(
        {
            data: document.getElementById("data").value.trim(),
            box: document.getElementById("box").value,
            border: document.getElementById("border").value,
            fill: document.getElementById("fill").value,
            back: document.getElementById("back").value,
            error_correction: document.getElementById("error_correction").value,
        }
    );
    return "/qrcode.png?" + params.toString();
}

// Helper: Build the qrcode.svg URL with current form values:
function svgUrl() {
    const params = new URLSearchParams(
        {
            data: document.getElementById("data").value.trim(),
            scale: document.getElementById("scale").value, // the scale should apply to SVG border
            border: document.getElementById("border").value,
            dark: document.getElementById("fill_svg").value,
            light: document.getElementById("background_svg").value,
            error_correction: document.getElementById("error_correction").value,
        }        
    );
    return "/qrcode.svg?" + params.toString();
}

// Main function:
// 1. Regenerate URLs for PNG and SVG
function update() {
    const uPng = pngUrl();
    const uSVG = svgUrl();

// 2a. Updating the image preview for PNG
    img.src = uPng;

// 2b. Updating the SVG preview image
    if (svgImg) {
        svgImg.src = uSVG;
    }

// 3a. Enabling PNG download button and setting click behavior
    dlBtnPNG.disabled = false;
    dlBtnPNG.onclick = () => {
        // Create a temporary anchor to use the download attribute
        const a = document.createElement("a");
        a.href = uPng;
        a.download = "qrcode.png";
        document.body.appendChild(a);
        a.click(); // trigger download
        a.remove(); // clean up
    };  

// 3b. Enabling SVG download button and setting click behavior
    dlBtnSVG.disabled = false;
    dlBtnSVG.onclick = () => {
        const a = document.createElement("a");
        a.href = uSVG;
        a.download = "qrcode.svg";
        document.body.appendChild(a);
        a.click();
        a.remove();
    };
}

// Update previews; prevent full-page reload
form.addEventListener("submit", (e) => {
    e.preventDefault();
    update();
});

// Recomputing previews on relevant input changes
["data", "box", "border", "fill", "back", "error_correction", "scale", "fill_svg", "background_svg"].forEach(id => {
    document.getElementById(id).addEventListener("input", update);
});

// Initial preview update on first load - UX parity, instant feedback
update();
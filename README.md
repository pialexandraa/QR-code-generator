Title: **QR code generator**

Technical implementation: The web-app uses **Flask**, **Pillow** for image manipulation, and for the QR code processes (encoding, matrix generation) the libraries **qrcode** and **segno**.

![URL/link address > QR code:](https://github.com/pialexandraa/QR-code-generator/blob/main/assets/Screenshot_1.png)

![Random text > QR code: ](https://github.com/pialexandraa/QR-code-generator/blob/main/assets/Screenshot_2.png)

Description: I kept this simple, since I wanted to write a "Pythonic" app. The implementation works well, the UI is clean, it scales, the QR codes can be updated/downloaded, and the user sees the changes in real-time. The application is designed to be web-based, and it is supposed to touch on the following points:

1. I followed strict implementation rules, with extensive (in-code) documentation notes/comments.
2. I did some "lazy code writing," meaning that I left most of the heavy work to be done by the libraries. For example, what I mean by that is: for the QR code version, I let the library do the matrix search and match (1..40). So I did not explicitly define the version (manually); if you see in the code, initially, I had the version defined, and later I decided to comment it out and use the automatic assignment. What I did was set the version to “None” and called qrcode.make(fit=True) => the version is picked automatically, and potential DataOverflow errors are avoided.
3. The UI is minimal, but the QR code generation, editing, and download work, as indicated by the listed options.
4. On the SVG side, it was initially set to be displayed via an iframe, which would visually cause issues or misalignment => I switched to an image type of tag (mainly because this is a pretty static application and dynamic behavior was not expected nor needed here).

import urllib.request
import json

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

images = ["flower.jpg", "insect.jpg", "bird.jpg", "mug.jpg"]

for img in images:
    with open(f"scratch/{img}", "rb") as f:
        photo_data = f.read()

    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{img}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8")
    footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = header + photo_data + footer

    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/identify",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )

    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"{img}: {res['name']} ({res['kind']}, {res['confidence']}%, {res['seconds']}s) - fact: {res['fun_fact']}")

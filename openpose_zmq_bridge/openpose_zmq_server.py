import os
import sys
import zmq
import base64
import numpy as np
import cv2
import json
from sys import platform

# ---- Setup OpenPose Path ----
try:
    root_path = "/Users/naveenschoudhary/Developer/company/openpose"  # 👈 Change this to your OpenPose directory

    # Windows
    if platform == "win32":
        sys.path.append(os.path.join(root_path, 'build/python/openpose/Release'))
        os.environ['PATH'] = os.path.join(root_path, 'build/bin') + ';' + os.environ['PATH']
    # Linux/macOS
    else:
        sys.path.append(os.path.join(root_path, 'build/python'))
        sys.path.append(os.path.join(root_path, 'build/python/openpose'))

    import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    print('Error: ' + str(e))
    sys.exit(-1)


params = {
    "model_folder": os.path.join(root_path, "models"),
    "number_people_max": 1,
    "face": True,          
    "hand": True,          
}

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# ---- Start ZeroMQ Server ----
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:8888")

print("✅ OpenPose ZMQ server running on port 8888...")

while True:
    # Receive and decode image
    b64_data = socket.recv()
    print("Received image")
    # print("Received image", b64_data)
    image_bytes = base64.b64decode(b64_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run OpenPose
    datum = op.Datum()
    datum.cvInputData = img
    
    # Create a VectorDatum object
    datumsPtr = op.VectorDatum()
    datumsPtr = op.VectorDatum([datum])  # Option 2
    opWrapper.emplaceAndPop(datumsPtr)

    keypoints = datum.poseKeypoints.tolist() if datum.poseKeypoints is not None else []
    print("Keypoints----", len(keypoints))
    # Send keypoints back
    socket.send_json({"pose_keypoints": keypoints})

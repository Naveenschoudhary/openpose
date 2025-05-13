# Model Files

The following model files are too large for GitHub and need to be downloaded separately:

1. `models/face/pose_iter_116000.caffemodel` (146.60 MB)
2. `models/hand/pose_iter_102000.caffemodel` (140.52 MB)
3. `models/pose/body_25/pose_iter_584000.caffemodel` (99.86 MB)

You can download these files by running the script in the models directory:

```bash
cd models
./getModels.sh  # for Linux/Mac
# or
getModels.bat  # for Windows
```

This will download all the necessary model files from the official OpenPose repository.

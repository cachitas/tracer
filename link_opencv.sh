# OpenCV must have been built system wide with this Python version. Edit me!!!
PYTHON=python3.4

VENV_LIB=/home/hugo/.virtualenvs/tracer/lib/$PYTHON
VENV_CV2=$VENV_LIB/

# Find cv2 library for the global Python installation.
GLOBAL_CV2=$($PYTHON -c 'import cv2; print(cv2)' | awk '{print $4}' | sed s:"['>]":"":g)

# Link global cv2 library file inside the virtual environment.
# Hard copy, no symlink
cp -uv $GLOBAL_CV2 $VENV_CV2

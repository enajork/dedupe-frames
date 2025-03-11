## Install modules
- Run `pip install opencv-python numpy scikit-image`

## Usage
- Edit the script if you wish to change the input and output name. By default, the script targets the input named "timelapse.mov" and outputs to "output.mov".
- Run `python dedupe-frames.py`

### Note
- This script is rather slow. It does not use multithreading or hardware acceleration. Use it accordingly.

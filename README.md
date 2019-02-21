# Tensorflow C++ API Install (Windows)
This is tools for export the header/lib/dll files of tensorflow
## Dependencies
- glog
- gflags

## Usage
- Build libtensorflow_cc.so or libtensorflow.so with bazel.
- assume you have get libtensorflow_cc.so or lib libtensorflow.so, execute install.py to get tensorflow c++ header and lib/dll, example:
```
python install.py -input=E:/Project/tensorflow -output=A:/C++/Tensorflow/v1.12.0 -msvc=v140 platform=x64
```
- Create your project with vs, and add A:/C++/Tensorflow/v1.12.0/Tensorflow.props to your project in Property Manager

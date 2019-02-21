import os
import shutil
import glog
import gflags

gflags.DEFINE_string('input', 'E:/C++/tensorflow', 'The root of tensorlfow source')
gflags.DEFINE_string('output', 'A:/C++/Tensorflow/v1.12.0', 'The root of output library')
gflags.DEFINE_list('libs', 'tensorflow_cc', "The name of tensorflow lib, eg tensorflow_cc, tensorflow")
gflags.DEFINE_string('msvc', 'v140', 'The version of platform toolset, eg: v140, v141 or v120')
gflags.DEFINE_string('platform', 'x64', 'The name(win32 or x64) of platform.')
flags = gflags.FLAGS


def copy(input_root, output_root, ext='.h'):
  for path, dirs, files in os.walk(input_root):
    for filename in files:
      if ext is not None:
        if not filename.endswith(ext):
          continue
      if not os.path.exists(path):
        path = '' if len(path) == 0 else '/' + path
        output_dir = output_root + path
        input_dir = input_root + path
      else:
        path = path.replace('\\', '/')
        input_dir = path
        output_dir = output_root + path.replace(input_root, '')
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      output_filename = output_dir + '/' + filename
      if os.path.exists(output_filename):
        os.remove(output_filename)
      input_filename = input_dir + '/' + filename
      glog.info('%s -> %s' % (input_filename, output_filename))
      shutil.copyfile(input_filename, output_filename)


def main():
  input_root = flags.input
  output_root = flags.output

  def copy_tensorflow_include():
    copy(input_root + '/tensorflow/core', output_root + '/include/tensorflow/core')
    copy(input_root + '/tensorflow/cc', output_root + '/include/tensorflow/cc')
    copy(input_root + '/bazel-genfiles/tensorflow/cc', output_root + '/include/tensorflow/cc')
    copy(input_root + '/bazel-genfiles/tensorflow/core', output_root + '/include/tensorflow/core')

  def copy_eigen_include():
    copy(input_root + '/third_party/eigen3',
         output_root + '/include/third_party/eigen3', None)
    copy(input_root + '/bazel-tensorflow/external/eigen_archive/Eigen',
         output_root + '/include/Eigen', None)
    copy(input_root + '/bazel-tensorflow/external/eigen_archive/unsupported',
         output_root + '/include/unsupported', None)

  def copy_absl_include():
    copy(input_root + '/bazel-tensorflow/external/com_google_absl/absl', output_root + '/include/absl')

  def copy_protobuf_include():
    copy(input_root + '/bazel-tensorflow/external/protobuf_archive/src/google',
         output_root + '/include/google')

  def copy_tensorflow_library():
    input_dir = input_root + '/bazel-out/x64_windows-opt/bin/tensorflow'

    output_dir = output_root + '/%s/%s' % (flags.platform, flags.msvc)
    output_bin_dir = output_dir + '/bin'
    output_lib_dir = output_dir + '/lib'

    if not os.path.exists(output_bin_dir):
      os.makedirs(output_bin_dir)
    if not os.path.exists(output_lib_dir):
      os.makedirs(output_lib_dir)

    dpendencies = ''
    for filename in flags.libs:
      input_lib = input_dir + '/liblib%s.so.ifso' % filename
      input_dll = input_dir + '/lib%s.so' % filename
      dpendencies += '%s.lib;' % filename
      output_dll = output_bin_dir + '/%s.dll' % filename
      output_lib = output_lib_dir + '/%s.lib' % filename

      if os.path.exists(output_lib):
        os.remove(output_lib)
      if os.path.exists(output_dll):
        os.remove(output_dll)

      glog.info('%s -> %s' % (input_dll, output_dll))
      shutil.copyfile(input_dll, output_dll)
      glog.info('%s -> %s' % (input_lib, output_lib))
      shutil.copyfile(input_lib, output_lib)

    file = open('./Tensorflow.templet', 'r').read()
    open('%s/%s.props' % (output_root, "Tensorflow"), 'w').write(
      file.format(tensorflow_dir=output_root, tensorflow_dpendencies=dpendencies))

  copy_tensorflow_include()
  copy_eigen_include()
  copy_absl_include()
  copy_tensorflow_library()
  copy_protobuf_include()


if __name__ == '__main__':
  import sys

  flags(sys.argv)
  main()

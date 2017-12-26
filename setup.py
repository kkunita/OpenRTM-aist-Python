#!/usr/bin/env python
#
# @file setup.py
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2013
#     Noriaki Ando
#     Intelligent Systems Research Institute, National Institute of
#     Advanced Industrial Science and Technology (AIST), Japan All
#     rights reserved.
#
#------------------------------------------------------------
# How to update this script:
#
# 1. Change version number for "pkg_*_version"
# 2. Change version number in package description "pkg_desc"
# 3. If new author should be added, add he/she in the "pkg_author"
# 4. And modify other pkg_* variables if necessary.
#
# How to use this setup.py script
#
# Usage:
#   setup.py option (build_*|clean_*|install_*|sdist_*) command option
#
# * Build
#   Build command will perform IDL compilation and document generation
#   by doxygen.
#
#   build: perform IDL compilation and document generation
#   build_core: IDL compilation of core modules
#   build_example: IDL compilation of examples
#   build_doc: Document generation by doxygen
#
# * Clean
#   Clean command delete all the generated files, including CORBA
#   stubs and documentation files.
#
#   clean: Cleanup all files generated by build_* commands
#   clean_core: Cleanup generated stubs in core
#   clean_example: Cleanup documentation files
#   clean_doc: Cleanup generated stubs in examples
#
# * Installation
#   This script installs python module files and others according to the
#   following rules
#
#   install: installing all files. 
#   install_core: installing core libraries.
#     core modules: -> <prefix>/lib/pythonX.Y/dist-pacakges/OpenRTM_aist/
#       OpenRTM-aist.pth
#       OpenRTM_aist/*.py
#       OpenRTM_aist/RTM_IDL/*_idl.py
#       OpenRTM_aist/RTM_IDL/(OpenRTM|RTC|RTM|SDOPackage)/*.py
#       OpenRTM_aist/RTM_IDL/(OpenRTM|RTC|RTM|SDOPackage)__POA/*.py
#     data files: -> <prefix>/lib/pythonX.Y/dist-pacakges/OpenRTM_aist/
#       OpenRTM_aist/RTM_IDL/*.idl
#       OpenRTM_aist/RTM_IDL/device_interfaces/*.idl
#     ext modules: -> <prefix>/lib/openrtm-x.y/python
#       OpenRTM_aist/ext/sdo/observer/*.(py|idl|conf|sh) unix
#       OpenRTM_aist/ext/sdo/observer/*.(py|idl|conf|bat) win32
#   install_doc
#     document files: -> <prefix>/share/openrtm-x.y/doc/python/
#       OpenRTM_aist/docs/ClassReference-jp
#       OpenRTM_aist/docs/ClassReference-en
#   install_example
#     example files: -> <prefix>/share/openrtm-x.y/example/python/
#       OpenRTM_aist/examples/*
#
# * Source distribution
#   This command creates source distribution packages.
#
#   sdist: create all source distribution packages
#   sdist_tgz: create tgz type  source distribution packages
#   sdist_zip: create zip type  source distribution packages
#
#------------------------------------------------------------

#==============================
# Package version definition
#==============================
pkg_major_version = "1"
pkg_minor_version = "2"
pkg_revision_num  = "0"

#============================================================
# MODIFICATION IS ALLOWED IF IT IS NEED TO MODIFY.
#============================================================
pkg_name      = "OpenRTM-aist-Python"
pkg_shortver  = pkg_major_version + "." + pkg_minor_version
pkg_version   = pkg_shortver + "." + pkg_revision_num
pkg_desc      = "Python modules for OpenRTM-aist-" + pkg_shortver
pkg_author    = "Shinji Kurihara and Noriaki Ando"
pkg_email     = "n-ando@aist.go.jp"
pkg_url       = "http://openrtm.org/"
pkg_license   = "LGPL"
pkg_long_desc = """\
OpenRTM-aist is a reference implementation of RT-Middleware and
RT-Component framework. RT-Component (RTC) is a component model
standardized in OMG (Object Management Group) as Robotic Technology
Component Specification 1.0 (formal/08-04-04,
http://www.omg.org/spec/RTC/1.0).  OpenRTM-aist is being developed and
distributed by Intelligent Systems Research Institute, National
Institute of Advanced Industrial Science and Technology (AIST), Japan.
Please see http://openrtm.org/ for more details."""
pkg_usage     = """\
Common commands: (see '--help-commands' for more)

  setup.py build            will compile IDL files and documentation
  setup.py build_core       will compile core IDL files
  setup.py build_example    will compile examples' IDL files
  setup.py build_doc        will compile documentation
  setup.py clean            will cleanup all generated files
  setup.py clean_core       will cleanup stubs in core libraries
  setup.py clean_example    will cleanup stubs in examples
  setup.py clean_doc        will cleanup generated documentation files
  setup.py install          will perform build and install the package
  setup.py install_core     will perform build core and install the package
  setup.py install_example  will perform build examples and install them
  setup.py install_doc      will process documentation and install them
  setup.py sdist            will create source package in tgz and zip
  setup.py sdist_tgz        will create tgz source package
  setup.py sdist_zip        will create zip source package
"""

#============================================================
# importing modules
#============================================================
import os,os.path
import sys
import string
if sys.version_info[0] == 2:
  import commands
else:
  import subprocess as commands
import glob
import shutil
from distutils import core
from distutils.core import Command
from distutils import cmd
from distutils import log
from distutils import util
from distutils import dir_util
from distutils import errors
from distutils import version
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.sdist import sdist
from distutils.command.install import install
from distutils.command.install_lib import install_lib
from distutils.command.install_data import install_data

#------------------------------------------------------------
# Getting OS type
#------------------------------------------------------------
def os_is():
  if os.sep == '/':
    return "unix"
  elif os.sep == ':':
    return None
  elif os.sep == '\\':
    return "win32"
  else:
    return None

#============================================================
# Directory settings for file list
#============================================================
current_dir  = os.getcwd()
#
# core settings
#
module_dir = "OpenRTM_aist"
openrtm_core_packages = [
  "OpenRTM_aist",
  "OpenRTM_aist.RTM_IDL",
  "OpenRTM_aist.RTM_IDL.OpenRTM",
  "OpenRTM_aist.RTM_IDL.OpenRTM__POA",
  "OpenRTM_aist.RTM_IDL.RTC",
  "OpenRTM_aist.RTM_IDL.RTC__POA",
  "OpenRTM_aist.RTM_IDL.RTM",
  "OpenRTM_aist.RTM_IDL.RTM__POA",
  "OpenRTM_aist.RTM_IDL.SDOPackage",
  "OpenRTM_aist.RTM_IDL.SDOPackage__POA",
  "OpenRTM_aist.RTM_IDL.device_interfaces",
  ]
openrtm_ext_packages = [
  "OpenRTM_aist.ext",
  "OpenRTM_aist.ext.sdo",
  "OpenRTM_aist.ext.sdo.observer",
  "OpenRTM_aist.ext.ssl",
  ]
openrtm_utils_packages = [
  "OpenRTM_aist.utils",
  "OpenRTM_aist.utils.rtcd",
  "OpenRTM_aist.utils.rtcprof",
  "OpenRTM_aist.utils.rtc-template",
  "OpenRTM_aist.utils.rtm-naming",
  ]

#
# IDL settings
#
baseidl_dir   = "OpenRTM_aist/RTM_IDL"
baseidl_files = [
  "BasicDataType.idl",
  "DataPort.idl",
  "ExtendedDataTypes.idl",
  "InterfaceDataTypes.idl",
  "Manager.idl",
  "OpenRTM.idl",
  "RTC.idl",
  "SDOPackage.idl",
  "SharedMemory.idl",
  "IORProfile.idl",
  "ExtendedFsmService.idl",
  "DataPort_OpenRTM.idl"
  ]
baseidl_mods  = ["RTM", "RTC", "SDOPackage", "OpenRTM"]
baseidl_path  = os.path.normpath(current_dir + "/" + baseidl_dir)

#
# scripts settings
#
pkg_scripts_unix  = ['OpenRTM_aist/utils/rtcd/rtcd_python',
                     'OpenRTM_aist/utils/rtcprof/rtcprof_python']
pkg_scripts_win32 = ['OpenRTM_aist/utils/rtcd/rtcd.py',
                     'OpenRTM_aist/utils/rtcd/rtcd_python.exe',
                     'OpenRTM_aist/utils/rtcd/rtcd_python.bat',
                     'OpenRTM_aist/utils/rtcprof/rtcprof_python.py',
                     'OpenRTM_aist/utils/rtcprof/rtcprof_python.bat']
#
# ext modules
#
ext_dir               = "OpenRTM_aist/ext"
target_ext_dir        = "lib/openrtm-" + pkg_shortver + "/python"
ext_match_regex_unix  = ".*\.(py|conf|sh|xml|idl)$"
ext_match_regex_win32 = ".*\.(py|conf|bat|xml|idl)$"
#
# examples
#
example_dir           = "OpenRTM_aist/examples"
target_example_dir    = "share/openrtm-" + pkg_shortver + "/components/python"
example_match_regex   = ".*\.(py|conf|sh|xml|idl)$"
example_path          = os.path.normpath(current_dir + "/" + example_dir)
#
# documents
#
document_dir          = "OpenRTM_aist/docs"
target_doc_dir        = "share/openrtm-" + pkg_shortver + "/doc/python"
document_match_regex  = ".*\.(css|gif|png|html||hhc|hhk|hhp)$"
document_path         = os.path.normpath(current_dir + "/" + document_dir)


################################################################################
# DO NOT CHANGE FROM HERE !!!
################################################################################

#============================================================
# utility functions
#============================================================
#------------------------------------------------------------
# Creating file list to be passed to distutils.core.setup
#
# This function creates the following file list.
#
# [(<install dir name0>, [<path to file0 from current dir>, <file1>, ...]),
#  (<install dir name1>, [file2, file3, ....]), ...]
#
# usage:
#   create_filelist(start_path, subs_path, target_path, regex_match)
#
# @param start_path A path to start walking through recursively.
# @param subs_path  A partial path to be removed from the file pathes obtained.
# @param target_path Target directory shere you want to install the files.
# @param regex_match A regular expression to match the files to be installed.
#
# example:
# Now we assume that the following arguments are set to create_filelist()
# start_path  = OpenRTM_aist/examples/
# subs_path   = OpenRTM_aist/examples/
# target_path = share/openrtm-1.2/components/python/
# regex_match = .*\.py$
#
# A file matched: OpenRTM_aist/examples/SimpleIO/ConsoleIn.py
# "OpenRTM_aist/examples" (subs_path) is removed from the
# path. obtained file path: SimpleIO/ConsoleIn.py is merged
# target_path, and then we get final target path
# <prefix>/share/openrtm-1.2/components/python/SimpleIO/ConsoleIn.py
#
#------------------------------------------------------------
def create_filelist(start_path, subs_path, target_path, regex_match, 
not_included_modules=[]):
  filelist = []
  temp_hash = {}
  if start_path[-1] != "/": start_path += "/"
  if subs_path[-1] != "/": subs_path += "/"
  import re
  for root, dirs, files in os.walk(start_path):
    if root.replace("\\","/") in not_included_modules:
      continue
    for filename in files:
      if re.match(regex_match, filename):
        subdir = re.sub(subs_path, "", root)
        dir_name = os.path.join(target_path, subdir)
        file_path = os.path.join(root, filename)
        if not dir_name in temp_hash:
          temp_hash[dir_name] = []
        temp_hash[dir_name].append(file_path)

  for k in temp_hash.keys():
    filelist.append((k, temp_hash[k]))
  return filelist

#------------------------------------------------------------
# convert_file_code()
#
# converting file encoding and CR-LF code
#
# Usage:
#  convert_file_code(file_name, to_code, to_crlf_code)
#
# Example:
#    -- converting to DOS/Windows code (SJIS/CRLF) --
#    convert_file_code("hoge.txt", "shift_jis", "\r\n")
#
#    -- converting to UNIX/Mac OS X code (EUC/LF) --
#    convert_file_code("hoge.txt", "euc_jp", "\n")
#
#------------------------------------------------------------
def convert_file_code(file_name, char_code, crlf_code, hint=None):
  import codecs
  import os
  def conv_encoding(data, to_enc="utf_8"):
    default_lookup = ('utf_8',
                      'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                      'shift_jis', 'shift_jis_2004','shift_jisx0213',
                      'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2',
                      'iso2022_jp_3', 'iso2022_jp_ext',
                      'latin_1', 'ascii')
    if hint:
      lookup = (hint, 'ascii', 'shift_jis', 'euc_jp')
    else:
      lookup = default_lookup
    for encoding in lookup:
      try:
        data = data.decode(encoding)
        break
      except:
        pass
    if isinstance(data, unicode):
      return data.encode(to_enc)
    else:
      return data
    # end of conv_encoding()
  temp_fname = file_name + ".tmp"
  outfd = open(temp_fname, "w")
  def coding_name(coding):
    conv = {"euc_jp": "euc-jp",
            "shift_jis": "cp932"}
    if coding in conv:
      return conv[coding]
    return coding
  sub_str = "coding: " + coding_name(char_code)
  import re
  infd = open(file_name, "r")
  for line in infd:
    try:
      outdata = conv_encoding(line.rstrip('\r\n'), char_code)
      outdata = re.sub("coding: [^ ]*", sub_str, outdata)
      outdata = re.sub("encoding: [^ ]*", sub_str, outdata)
    except Exception as e:
      print("Exception cought in " + file_name + ": " + line)
      print(e)
      infd.close()
      outfd.close()
      os.remove(temp_fname)
      sys.exit(1)
    outfd.write(outdata + crlf_code)
  infd.close()
  os.remove(file_name)
  outfd.close()
  os.rename(temp_fname, file_name)

#------------------------------------------------------------
# compiling IDL files
#------------------------------------------------------------
def compile_idl(idl_compiler, include_dirs, current_dir, files):
  """
  compile_idl
    - idl_compiler: [string] path to omniidl executable
    - include_dirs: [list] path list for include directories
    - current_dir : [string] directory where stubs are generated
    - files       : [list] IDL file list
  """
  # create command and option list
  cmd = [idl_compiler, "-bpython"]
  if include_dirs: cmd += ["-I" + inc for inc in include_dirs]
  if current_dir : cmd += ["-C" + current_dir]
  cmd += files
  # function to be given dist.util.execute
  def exec_idl_compile(cmd_str):
    #cmdline = string.join(cmd_str)
    cmdline = " ".join(cmd_str)
    if os_is() == "win32":
      os.system(cmdline)
      return
    log.info(cmdline)
    status, output = commands.getstatusoutput(cmdline)
    log.info(output)
    if status != 0:
      raise errors.DistutilsExecError("Return status of %s is %d" %
                                      (cmd, status))
    return
  # compile IDL by using dist.util.execute
  util.execute(exec_idl_compile, [cmd],
               "Generating python stubs from IDL files")

#------------------------------------------------------------
# compiling doxygen
#------------------------------------------------------------
def create_doc(doxygen_conf, target_dir):
  """
  create_doc
    - doxygen_conf: [string] path to Doxygen's conf file
    - target_dir  : [string] directory to where doxygen generates documentation
  """
  def exec_doxygen(cmd):
    # remove target dir
    if os.path.exists(target_dir + "/html/index.html"):
      return
    if os.path.exists(target_dir):
      shutil.rmtree(target_dir)

    #cmdline = string.join(cmd)
    cmdline = " ".join(cmd)
    if os_is() == "win32":
      os.system(cmdline)
      return
    log.info(cmdline)
    status, output = commands.getstatusoutput(cmdline)
    log.info(output)
    if status != 0:
      raise errors.DistutilsExecError("Return status of %s is %d" %
                                      (cmd, status))
    return
  # compile IDL by using dist.util.execute
  docdir = os.path.dirname(doxygen_conf)
  tmp = os.getcwd()
  os.chdir(docdir)
  cmd = ["doxygen", doxygen_conf]
  util.execute(exec_doxygen, [cmd],
               "Generating documentation")
  os.chdir(tmp)


#============================================================
# command classes
#
# build
#   build_core
#   build_example
#   build_doc
# clean
#   clean_core
#   clean_example
# clean_doc (clean_doc is not subcommand of clean, because
#            documentation files are included sdist pakcage
#            )
# sdist
#   sdist_tgz
#   sdist_zip
# install
#   install_core
#   install_example
#   install_doc
#============================================================

#============================================================
# build command family
#============================================================
#------------------------------------------------------------
# "build" command
#------------------------------------------------------------
class build_all(build):
  """
  This class is a parent command of build to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Generate python CORBA stubs from IDL files and documentation"
  user_options = build.user_options + [
    ("omniidl=", "i",
     "omniidl program used to build stubs"),
    ("idldir=",  "i",
     "directory where IDL files reside"),
    ("doxygen=",  "d",
     "path to doxygen executable")
    ]

  def initialize_options(self):
    self.omniidl = None
    self.idldir  = None
    self.doxygen = None
    build.initialize_options(self)
    return

  def finalize_options(self):
    build.finalize_options(self)
    if not self.omniidl:
      self.omniidl = "omniidl"

    if not self.idldir:
      self.idldir = baseidl_path

    if not self.doxygen:
      self.doxygen = "doxygen"
    # Transferring options to sub-commands
    self.distribution.omniidl = self.omniidl
    self.distribution.idldir  = self.idldir
    self.distribution.doxygen = self.doxygen

  def run(self):
    return build.run(self)

  # sub_command member attribute
  sub_commands = [
    ('build_core', None),
    ('build_doc',  None),
    ('build_example', None)
    ]

#------------------------------------------------------------
# "build_sub" base class
#------------------------------------------------------------
class build_sub(build):
  """
  This class is a subcommand base class for compiling IDL and
  generating stubs.
  """
  description = "Generate python CORBA stubs for core from IDL files"
  user_options = build.user_options + [
    ("omniidl=", "i",
     "omniidl program used to build stubs"),
    ("idldir=",  "d",
     "directory where IDL files reside")
    ]

  def initialize_options(self):
    self.idldir  = None
    self.omniidl = None
    build.initialize_options(self)

  def finalize_options(self):
    build.finalize_options(self)
    if not self.omniidl:
      if hasattr(self.distribution, "omniidl"):
        self.omniidl = self.distribution.omniidl
      else:
        self.omniidl = "omniidl"

    if not self.idldir:
      if hasattr(self.distribution, "idldir"):
        self.idldir = self.distribution.idldir
      else:
        self.idldir = None
    return

#------------------------------------------------------------
# "build_core" sub command
#------------------------------------------------------------
class build_core(build_sub):
  """
  This class is a subcommand of build command. The command compiles
  IDL files and generates CORBA stubs for core packages.
  """
  description = "Generate python CORBA stubs for core packages."
  def run(self):
    idldir = baseidl_path
    include_dirs = [baseidl_path]
    current_dir = baseidl_path
    idl_files   = [os.path.join(baseidl_path, f) for f in baseidl_files]
    compile_idl(self.omniidl, include_dirs, current_dir, idl_files)
    self.run_command("build_py")

from distutils.command.build_py import build_py as _build_py
class build_py(_build_py):
  """
  This class is a subcommand of build_core command. The command copies
  modules into build directory.
  # This class was created for only copying OpenRTM-aist.pth file
  """
  description = "Copying pure python modules into build directory."
  def run(self):
    # Preparering rtcprof_python.py for Windows
    if os_is() == "win32":
      rtcprof_dir = os.path.join("OpenRTM_aist", "utils", "rtcprof/")
      self.copy_file(os.path.join(rtcprof_dir, "rtcprof.py"),
                     os.path.join(rtcprof_dir, "rtcprof_python.py"))
    _build_py.run(self)
    # copying OpenRTM-aist.pth file
    self.copy_file(os.path.join(".", "OpenRTM-aist.pth"), self.build_lib,
                   preserve_mode=False)

#------------------------------------------------------------
# "build_example" sub command
#------------------------------------------------------------
class build_example(build_sub):
  """
  This class is a subcommand of build command. The command compiles
  IDL files and generates CORBA stubs for example packages.
  """
  description = "Generate python CORBA stubs for example packages."
  def run(self):
    # SimpleService
    current_dir  = os.path.join(example_dir, "SimpleService")
    include_dirs = [baseidl_path, current_dir]
    idl_files    = [os.path.join(current_dir, "MyService.idl")]
    compile_idl(self.omniidl, include_dirs, current_dir, idl_files)

    # AutoTest
    current_dir  = os.path.join(example_dir, "AutoTest")
    include_dirs = [baseidl_path, current_dir]
    idl_files    = [os.path.join(current_dir, "AutoTestService.idl")]
    compile_idl(self.omniidl, include_dirs, current_dir, idl_files)


#------------------------------------------------------------
# "build_doc" sub command
#------------------------------------------------------------
class build_doc(build):
  """
  This class is a subcommand of build command. The command generates
  documentation from source code.
  """
  description = "Generate documentation from source code."
  user_options =  build.user_options + [
    ("doxygen=", "d",
     "path to doxygen executable")
    ]

  def initialize_options(self):
    self.doxygen = None
    build.initialize_options(self)

  def finalize_options(self):
    build.finalize_options(self)
    if not self.doxygen:
      if hasattr(self.distribution, "doxygen"):
        self.doxygen = self.distribution.doxygen
      else:
        self.doxygen = "doxygen"

  def build_doc_common(self, infile, outfile):
    f_input = open(infile, 'r')
    src = f_input.read()
    f_input.close()
    dst = src.replace("__VERSION__", pkg_version)
    f_output = open(outfile, 'w')
    f_output.write(dst)
    f_output.close()
  
  def run(self):
    conf_in_file = os.path.normpath(document_path + "/Doxyfile_en.in")
    conf_file = os.path.normpath(document_path + "/Doxyfile_en")
    self.build_doc_common(conf_in_file, conf_file)
    target_dir = os.path.normpath(document_path + "/ClassReference-en")
    create_doc(conf_file, target_dir)

    conf_in_file = os.path.normpath(document_path + "/Doxyfile_jp.in")
    conf_file = os.path.normpath(document_path + "/Doxyfile_jp")
    self.build_doc_common(conf_in_file, conf_file)
    target_dir = os.path.normpath(document_path + "/ClassReference-jp")
    create_doc(conf_file, target_dir)


#============================================================
# clean command classes
#============================================================
def remove_stubs(target_dir, idl_files, module_names):
  files = [f.replace(".idl", "_idl.py") for f in idl_files]
  for f in files:
    file_path = os.path.normpath(target_dir + "/" + f)
    if os.path.exists(file_path):
      os.remove(file_path)
  # removing <modname> dirs and <modname__POA dirs
  for d in module_names:
    mod_dir = os.path.normpath(target_dir + "/" + d)
    if os.path.exists(mod_dir):
      shutil.rmtree(mod_dir)
    poa_dir = os.path.normpath(target_dir + "/" + d + "__POA")
    if os.path.exists(poa_dir):
      shutil.rmtree(poa_dir)

def remove_dirs(base_dir, dir_names):
  for d in dir_names:
    target_dir = os.path.normpath(base_dir + "/" + d)
    if os.path.exists(target_dir):
      shutil.rmtree(target_dir)

def remove_files(base_dir, file_names):
  for f in file_names:
    target_file = os.path.normpath(base_dir + "/" + f)
    if os.path.exists(target_file):
      os.remove(target_file)

#------------------------------------------------------------
# "clean" command
#------------------------------------------------------------
class clean_all(Command):
  """
  This class is a parent command of clean to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Generate python CORBA stubs from IDL files and documentation"
  user_options = []
  boolean_options = []
  def initialize_options(self):
    return

  def finalize_options(self):
    return

  def run(self):
    for cmd_name in self.get_sub_commands():
      self.run_command(cmd_name)
    return

  # sub_command member attribute
  sub_commands = [
    ('clean_core', None),
    ('clean_example', None),
    ('clean_doc', None)
    ]


#------------------------------------------------------------
# "clean_core" sub command
#------------------------------------------------------------
class clean_core(Command):
  """
  This class is a parent command of clean to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Removing generated CORBA stubs in core"
  user_options = []
  boolean_options = []

  def initialize_options(self):
    return
  def finalize_options(self):
    return
  def run(self):
    remove_stubs(baseidl_path, baseidl_files, baseidl_mods)
    remove_dirs('.', ["build"])
    remove_dirs('.', ["dist"])
    remove_files('.', ["MANIFEST"])

#------------------------------------------------------------
# "clean_example" sub command
#------------------------------------------------------------
class clean_example(Command):
  """
  This class is a parent command of clean to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Removing generated CORBA stubs in examples"
  user_options = []
  boolean_options = []

  def initialize_options(self):
    return
  def finalize_options(self):
    return
  def run(self):
    target_dir = os.path.normpath(example_dir + "/SimpleService")
    remove_stubs(target_dir, ["MyService.idl"], ["SimpleService"])
    target_dir = os.path.normpath(example_dir + "/AutoTest")
    remove_stubs(target_dir, ["AutoTestService.idl"], ["AutoTest"])

#------------------------------------------------------------
# "clean_doc" sub command
#------------------------------------------------------------
class clean_doc(Command):
  """
  This class is a parent command of clean to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Delete generated documentation files"
  user_options = []
  boolean_options = []

  def initialize_options(self):
    return
  def finalize_options(self):
    return
  def run(self):
    remove_dirs(document_path, ["ClassReference-en", "ClassReference-jp"])
    remove_files(document_path, ["Doxyfile_en", "Doxyfile_jp"])

#============================================================
# sdist command classes
#============================================================
from distutils.filelist import FileList

class sdist_all(sdist):
  def run(self):
    for cmd_name in self.get_sub_commands():
      self.run_command(cmd_name)
    return
  # sub_commands
  sub_commands = [
    ('sdist_tgz', None),
    ('sdist_zip',  None),
    ]

class sdist_tgz(sdist):
  def run(self):
    self.formats = ["gztar"]
    self.filelist = FileList()
    self.check_metadata()
    self.get_file_list()
    if self.manifest_only:
      return
    self.make_distribution()

class sdist_zip(sdist):
  def run(self):
    self.formats = ["zip"]
    self.filelist = FileList()
    self.check_metadata()
    self.get_file_list()
    if self.manifest_only:
      return
    """
    # converting character code into Shift-JIS
    import re
    for f in self.filelist.files:
      if not re.match('OpenRTM_aist.*\.py$', f): continue
      convert_file_code(f, "shift_jis", "\r\n", "euc_jp")
    """
    self.make_distribution()
    """
    # reverting character code
    for f in self.filelist.files:
      if not re.match('OpenRTM_aist.*\.py$', f): continue
      convert_file_code(f, "euc_jp", "\n", "shift_jis")
    """

#============================================================
# install command classes
#------------------------------------------------------------
# "install" command
#
# install_all: top level install command
#  +(install_lib)
#  +(install_scripts)
#  +(install_egg_info)
#  + install_core
#    + install_core_lib = install_lib
#    + install_core_scripts = install_scripts
#    + install_core_egg_info = install_egg_info
#  + install_example
#  + install_doc
#============================================================

class install_all(install):
  """
  This class is a parent command of install to compile IDL into CORBA
  stubs and to make documentation.
  """
  description = "Generate python CORBA stubs from IDL files and documentation"
  def run(self):
    for cmd_name in self.get_sub_commands():
      self.run_command(cmd_name) 
    return
  sub_commands = [('install_lib',     install.has_lib),
                  ('install_scripts', install.has_scripts),
                  ('install_data', install.has_data),
                  ('install_egg_info', lambda self:True),
                  ('install_example', lambda self:True),
                  ('install_doc', lambda self:True),
                  ]

class install_core(install):
  description = "Installing core modules and data files"
  sub_commands = [('install_core_lib',     install.has_lib),
                  ('install_core_scripts', install.has_scripts),
                  ('install_data', install.has_data),
                  ('install_core_egg_info', lambda self:True)
                  ]

from distutils.command.install_lib import install_lib as _install_lib
# sub-command "install_core_lib" which is called from install_core
class install_core_lib(_install_lib):
  def finalize_options (self):
    self.set_undefined_options('install_core',
                               ('build_lib', 'build_dir'),
                               ('install_lib', 'install_dir'),
                               ('force', 'force'),
                               ('compile', 'compile'),
                               ('optimize', 'optimize'),
                               ('skip_build', 'skip_build'),
                               )

from distutils.command.install_scripts import install_scripts as _install_scripts
# sub-command "install_core_script" which is called from install_core
class install_core_scripts(_install_scripts):
  def finalize_options (self):
    self.set_undefined_options('build', ('build_scripts', 'build_dir'))
    self.set_undefined_options('install_core',
                               ('install_scripts', 'install_dir'),
                               ('force', 'force'),
                               ('skip_build', 'skip_build'),
                               )
from distutils.command.install_egg_info import install_egg_info as _install_egg_info
# sub-command "install_core_egg_info" which is called from install_core
class install_core_egg_info(_install_egg_info):
  def finalize_options(self):
    self.set_undefined_options('install_core_lib',
                               ('install_dir','install_dir'))
    if hasattr(self, 'install_layout'):
      self.set_undefined_options('install_core',
                                 ('install_layout','install_layout'))
    if hasattr(self, 'prefix_option'):
      self.set_undefined_options('install_core',
                                 ('prefix_option','prefix_option'))
    _install_egg_info.finalize_options(self)


class install_example(install_data):
  description = "Installing example scripts"
  def initialize_options(self):
    self.example_files = None
    install_data.initialize_options(self)

  def finalize_options(self):
    install_data.finalize_options(self)
    self.example_files = self.distribution.example_files
    self.data_files = self.example_files

class install_doc(install_data):
  description = "Installing document files"
  def initialize_options(self):
    self.document_files = None
    install_data.initialize_options(self)

  def finalize_options(self):
    install_data.finalize_options(self)
    self.document_files = self.distribution.document_files
    self.data_files = self.document_files


from distutils.dist import Distribution

class MyDistribution(Distribution):
    def __init__(self, attrs=None):
        self.coredata_files= None
        self.example_files= None
        self.document_files= None
        Distribution.__init__(self, attrs)

#============================================================
# file list
#============================================================
#
# core package list
#
pkg_packages   = openrtm_core_packages \
               + openrtm_ext_packages  \
               + openrtm_utils_packages
#
# IDL file list
#
pkg_package_data_files = {
  'OpenRTM_aist': ['RTM_IDL/*.idl',
                   'RTM_IDL/device_interfaces/*.idl',
                   'ext/sdo/observer/*.conf',
                   'ext/sdo/observer/*.bat',
                   'ext/sdo/observer/*.sh',
                   'ext/sdo/observer/*.idl',
                   ],
  }
#
# scripts
#
if os_is() == "win32":
  pkg_scripts = pkg_scripts_win32
else:
  pkg_scripts = pkg_scripts_unix

#
# example file list -> MyDistribution.example_files
#
pkg_example_files   = create_filelist(example_dir,
                                      example_dir,
                                      target_example_dir,
                                      example_match_regex,
                                      ["OpenRTM_aist/examples/NXTRTC"])


#
# document file list -> MyDistribution.document_files
#
pkg_document_files_en = create_filelist(document_dir + "/ClassReference-en",
                                        document_dir,
                                        target_doc_dir,
                                        document_match_regex)
pkg_document_files_jp = create_filelist(document_dir + "/ClassReference-jp",
                                        document_dir,
                                        target_doc_dir,
                                        document_match_regex)
pkg_document_files = pkg_document_files_en + pkg_document_files_jp

#==============================
# main
#==============================
core.setup(name             = pkg_name,
           version          = pkg_version,
           description      = pkg_desc,
           author           = pkg_author,
           author_email     = pkg_email,
           url              = pkg_url,
           long_description = pkg_long_desc,
           license          = pkg_license,
           distclass        = MyDistribution,
           cmdclass         = { "build": build_all,
                                "build_core": build_core,
                                "build_py": build_py,
                                "build_example": build_example,
                                "build_doc": build_doc,
                                "clean": clean_all,
                                "clean_core": clean_core,
                                "clean_example": clean_example,
                                "clean_doc": clean_doc,
                                "install": install_all,
                                "install_core_lib": install_core_lib,
                                "install_core_scripts": install_core_scripts,
                                "install_core_egg_info": install_core_egg_info,
                                "install_core": install_core,
                                "install_example": install_example,
                                "install_doc": install_doc,
                                "sdist": sdist_all,
                                "sdist_tgz": sdist_tgz,
                                "sdist_zip": sdist_zip,
                                },
           packages         = pkg_packages,
           package_dir      = {module_dir: module_dir},
           package_data     = pkg_package_data_files,
           scripts          = pkg_scripts,
           example_files    = pkg_example_files,
           document_files   = pkg_document_files,
           )

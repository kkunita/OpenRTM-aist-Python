#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file LogstreamFile.py
# @brief File logger stream class
# @date $Date: $
# @author Nobuhiko Miyamoto <n-miyamoto@aist.go.jp>
# Copyright (C) 2017
#   Nobuhiko Miyamoto
#   National Institute of
#      Advanced Industrial Science and Technology (AIST), Japan
#   All rights reserved.
# $Id$



import OpenRTM_aist
import logging



##
# @if jp
# @class LogstreamFile
#
# @brief LogstreamFile ���饹
#
# 
#
#
# @else
# @class LogstreamFile
#
# @brief LogstreamFile class
#
#
# @endif
#
class LogstreamFile(OpenRTM_aist.LogstreamBase):
  """
  """
  s_logger = None
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.LogstreamBase.__init__(self)
    self.handlers = []

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    pass
    


  ##
  # @if jp
  # @brief ��������
  #
  # Logstream���饹�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
  # Properties����ɬ�פʾ����������ƳƼ������Ԥ���
  #
  # @param self
  # @param prop �������
  # @return
  #
  # @else
  # @brief Initializing configuration
  #
  # This operation would be called to configure in initialization.
  # In the concrete class, configuration should be performed
  # getting appropriate information from the given Properties data.
  #
  # @param self
  # @param prop Configuration information
  # @return
  #
  # @endif
  #
  def init(self, prop):
    self.logger = logging.getLogger("file")
    
    
    if LogstreamFile.s_logger is None:
      LogstreamFile.s_logger = self
      
      logging.PARANOID  = logging.DEBUG - 3
      logging.VERBOSE   = logging.DEBUG - 2
      logging.TRACE     = logging.DEBUG - 1
      logging.FATAL     = logging.ERROR + 1

      logging.addLevelName(logging.PARANOID,  "PARANOID")
      logging.addLevelName(logging.VERBOSE,   "VERBOSE")
      logging.addLevelName(logging.TRACE,     "TRACE")
      logging.addLevelName(logging.FATAL,     "FATAL")
      
    files = prop.getProperty("file_name")
    files = [s.strip() for s in files.split(",")]

    

    

    for f in files:
      self.addHandler(f)

    
        
    return True


  ##
  # @if jp
  # @brief �������ϥϥ�ɥ��ɲ�
  #
  #
  # @param self
  # @param f �������ϥե�����̾���⤷����stdout
  # @return
  #
  # @else
  # @brief 
  #
  #
  # @param self
  # @param f 
  # @return
  #
  # @endif
  #
  def addHandler(self, f):
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    tmp = [f]
    OpenRTM_aist.eraseHeadBlank(tmp)
    OpenRTM_aist.eraseTailBlank(tmp)
    f = tmp[0]
    handlers = self.logger.handlers
    for h in handlers:
      if h.get_name() == f:
        return False

    tmp = [f]
    fname = OpenRTM_aist.StringUtil.normalize(tmp)
      
    if fname == "stdout":
      ch = logging.StreamHandler()
      ch.setLevel(logging.NOTSET)
      ch.setFormatter(formatter)
      ch.set_name(f)
      self.logger.addHandler(ch)
      self.handlers.append(ch)
      return True

    else:
      fhdlr = logging.FileHandler(fname)
      mhdlr = logging.handlers.MemoryHandler(1024,logging.NOTSET, fhdlr)
      fhdlr.setFormatter(formatter)
      mhdlr.set_name(f)
      self.logger.addHandler(mhdlr)
      self.handlers.append(mhdlr)
      self.logger.setLevel(logging.NOTSET)
      return True

  ##
  # @if jp
  # @brief ����ʸ�����������Ϥ���
  #
  #
  # @param self
  # @param msg���������Ϥ���ʸ����
  # @param level ������٥�
  # @return
  #
  # @else
  # @brief 
  #
  #
  # @param self
  # @param msg
  # @param level
  # @return
  #
  # @endif
  #
  def log(self, msg, level):
    if level == OpenRTM_aist.Logger.FATAL:
      self.logger.log(logging.FATAL,msg)
    elif level == OpenRTM_aist.Logger.ERROR:
      self.logger.error(msg)
    elif level == OpenRTM_aist.Logger.WARN:
      self.logger.warning(msg)
    elif level == OpenRTM_aist.Logger.INFO:
      self.logger.info(msg)
    elif level == OpenRTM_aist.Logger.DEBUG:
      self.logger.debug(msg)
    elif level == OpenRTM_aist.Logger.TRACE:
      self.logger.log(logging.TRACE,msg)
    elif level == OpenRTM_aist.Logger.VERBOSE:
      self.logger.log(logging.VERBOSE,msg)
    elif level == OpenRTM_aist.Logger.PARANOID:
      self.logger.log(logging.PARANOID,msg)
    else:
      return False
      
    return True


  ##
  # @if jp
  # @brief ������٥�����
  #
  #
  # @param self
  # @param level ������٥�
  # @return
  #
  # @else
  # @brief 
  #
  #
  # @param self
  # @param level
  # @return
  #
  # @endif
  #
  def setLogLevel(self, level):
    if level == OpenRTM_aist.Logger.INFO:
      self.logger.setLevel(logging.INFO)
    elif level == OpenRTM_aist.Logger.FATAL:
      self.logger.setLevel(logging.FATAL)
    elif level == OpenRTM_aist.Logger.ERROR:
      self.logger.setLevel(logging.ERROR)
    elif level == OpenRTM_aist.Logger.WARN:
      self.logger.setLevel(logging.WARNING)
    elif level == OpenRTM_aist.Logger.DEBUG:
      self.logger.setLevel(logging.DEBUG)
    elif level == OpenRTM_aist.Logger.SILENT:
      self.logger.setLevel(logging.NOTSET)
    elif level == OpenRTM_aist.Logger.TRACE:
      self.logger.setLevel(logging.TRACE)
    elif level == OpenRTM_aist.Logger.VERBOSE:
      self.logger.setLevel(logging.VERBOSE)
    elif level == OpenRTM_aist.Logger.PARANOID:
      self.logger.setLevel(logging.PARANOID)
    else:
      self.logger.setLevel(logging.INFO)



  ##
  # @if jp
  # @brief ��λ����
  #
  #
  # @param self
  # @return
  #
  # @else
  # @brief 
  #
  #
  # @param self
  # @return
  #
  # @endif
  #
  def shutdown(self):
    for h in self.handlers:
      logging.Handler.close(h)
    
    LogstreamFile.s_logger = None
    self.handlers = []
    return True


def LogstreamFileInit():
  OpenRTM_aist.LogstreamFactory.instance().addFactory("file",
                                                      OpenRTM_aist.LogstreamFile,
                                                      OpenRTM_aist.Delete)

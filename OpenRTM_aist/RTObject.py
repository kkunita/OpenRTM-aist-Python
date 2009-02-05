#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RTObject.py
# @brief RT component base class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



from omniORB import any
from omniORB import CORBA
import string
import sys
import traceback

import OpenRTM, OpenRTM__POA
import RTC,RTC__POA
import SDOPackage,SDOPackage__POA
import OpenRTM_aist

ECOTHER_OFFSET = 1000

default_conf = [
  "implementation_id","",
  "type_name",         "",
  "description",       "",
  "version",           "",
  "vendor",            "",
  "category",          "",
  "activity_type",     "",
  "max_instance",      "",
  "language",          "",
  "lang_type",         "",
  "conf",              "",
  "" ]



##
# @if jp
# @brief RT����ݡ��ͥ�ȥ��饹
#
# ��RT����ݡ��ͥ�ȤΥ١����Ȥʤ륯�饹��
# Robotic Technology Component ������� lightweightRTComponent�μ������饹��
# ����ݡ��ͥ�Ȥε�ǽ���󶡤��� ComponentAction ���󥿡��ե�������
# ����ݡ��ͥ�ȤΥ饤�ե������������Ԥ������ LightweightRTObject �μ�����
# �󶡤��롣
# �ºݤ˥桼��������ݡ��ͥ�Ȥ����������ˤϡ�Execution Semantics ���б�
# �����ƥ��֥��饹�����Ѥ��롣<BR>
# (�����μ����Ǥ� Periodic Sampled Data Processing �Τߥ��ݡ��Ȥ��Ƥ��뤿�ᡢ
#  dataFlowComponent ��ľ�ܷѾ����Ƥ���)
#
# @since 0.2.0
#
# @else
#
# @endif
class RTObject_impl(OpenRTM__POA.DataFlowComponent):



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param manager �ޥ͡����㥪�֥�������(�ǥե������:None)
  # @param orb ORB(�ǥե������:None)
  # @param poa POA(�ǥե������:None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @param orb ORB
  # @param poa POA
  #
  # @endif
  def __init__(self, manager=None, orb=None, poa=None):
    if manager:
      self._manager = manager
      self._orb = self._manager.getORB()
      self._poa = self._manager.getPOA()
      self._portAdmin = OpenRTM_aist.PortAdmin(self._manager.getORB(),self._manager.getPOA())
    else:
      self._manager = None
      self._orb = orb
      self._poa = poa
      self._portAdmin = OpenRTM_aist.PortAdmin(self._orb,self._poa)
      
    self._created = True
    self._properties = OpenRTM_aist.Properties(defaults_str=default_conf)
    self._configsets = OpenRTM_aist.ConfigAdmin(self._properties.getNode("conf"))
    self._profile = RTC.ComponentProfile("","","","","","",[],None,[])
    
    self._SdoConfigImpl = OpenRTM_aist.Configuration_impl(self._configsets)
    self._SdoConfig = self._SdoConfigImpl.getObjRef()
    self._execContexts = []
    self._objref = self._this()
    self._sdoOwnedOrganizations = [] #SDOPackage.OrganizationList()
    self._sdoSvcProfiles        = [] #SDOPackage.ServiceProfileList()
    self._sdoOrganizations      = [] #SDOPackage.OrganizationList()
    self._sdoStatus             = [] #SDOPackage.NVList()
    self._ecMine = []
    self._ecOther = []

    return


  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  # 
  # @else
  # 
  # @brief destructor
  # 
  # @endif
  def __del__(self):
    return


  #============================================================
  # Overridden functions
  #============================================================

  ##
  # @if jp
  #
  # @brief ����������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_initialize ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤν���������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onInitialize(self):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ��λ�����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_finalize ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤν�λ�����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onFinalize(self):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���Ͻ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_startup ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤγ��Ͻ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onStartup(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ��߽����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_shutdown ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ���߽����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onShutdown(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �����������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_activated ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤγ����������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onActivated(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ������������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_deactivated ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ�������������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onDeactivated(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_execute ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤμ��������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� Two-Pass Execution��
  # �����ܤμ¹ԥѥ��Ȥ������Ū�˸ƤӽФ���롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onExecute(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���ǽ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_aborting ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ����ǽ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onAborting(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���顼�����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_error ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�ȤμºݤΥ��顼�����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onError(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �ꥻ�åȽ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_reset ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�ȤμºݤΥꥻ�åȽ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onReset(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �����ѹ������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_state_update ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤξ����ѹ������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� Two-Pass Execution��
  # �����ܤμ¹ԥѥ��Ȥ������Ū�˸ƤӽФ���롣
  #
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onStateUpdate(self, ec_id):
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ư������ѹ������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_rate_changed ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤξ����ѹ������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� ExecutionContext ��
  # �¹Ԥ��������줿�ݤ˸ƤӽФ���롣
  #
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onRateChanged(self, ec_id):
    return RTC.RTC_OK 


  #============================================================
  # RTC::LightweightRTObject
  #============================================================

  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC����������
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��ơ�ComponentAction::on_initialize
  # ������Хå��ؿ����ƤФ�롣
  # 
  # ����
  # - RTC �� Created���֤ξ��߽�������Ԥ��롣¾�ξ��֤ˤ�����ˤ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���ƤӽФ��ϼ��Ԥ��롣
  # - ���Υ��ڥ졼������ RTC �Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Initialize the RTC that realizes this interface.
  #
  # The invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_initialize.
  #
  # Constraints
  # - An RTC may be initialized only while it is in the Created state. Any
  #   attempt to invoke this operation while in another state shall fail
  #   with ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation
  #   directly; it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def initialize(self):
    # at least one EC must be attached
    if len(self._ecMine) == 0:
      return RTC.PRECONDITION_NOT_MET

    ret = self.on_initialize()
    if ret is not RTC.RTC_OK:
      return ret
    
    self._created = False

    # -- entering alive state --
    for ec in self._ecMine:
      ec.start()

    # ret must be RTC_OK
    return ret


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC ��λ����
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� ComponentAction::on_finalize()
  # ��ƤӽФ���
  #
  # ����
  # - RTC �� ExecutionContext �˽�°���Ƥ���֤Ͻ�λ����ʤ������ξ��ϡ�
  #   �ޤ��ǽ�� ExecutionContextOperations::remove_component �ˤ�äƻ��ä�
  #   ������ʤ���Фʤ�ʤ�������ʳ��ξ��ϡ����Υ��ڥ졼�����ƤӽФ���
  #   �����ʤ���� ReturnCode_t::PRECONDITION_NOT_ME �Ǽ��Ԥ��롣
  # - RTC �� Created ���֤Ǥ����硢��λ�����ϹԤ��ʤ���
  #   ���ξ�硢���Υ��ڥ졼�����ƤӽФ��Ϥ����ʤ����
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  # - ���Υ��ڥ졼������RTC�Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Finalize the RTC for preparing it for destruction
  # 
  # This invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_finalize.
  #
  # Constraints
  # - An RTC may not be finalized while it is participating in any execution
  #   context. It must first be removed with 
  #   ExecutionContextOperations::remove_component. Otherwise, this operation
  #   shall fail with ReturnCode_t::PRECONDITION_NOT_MET. 
  # - An RTC may not be finalized while it is in the Created state. Any 
  #   attempt to invoke this operation while in that state shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation directly;
  #  it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def finalize(self):
    if self._created:
      return RTC.PRECONDITION_NOT_MET
    
    # Return RTC::PRECONDITION_NOT_MET,
    # When the component is registered in ExecutionContext.
    if len(self._ecOther) is not 0:
      return RTC.PRECONDITION_NOT_MET

    ret = self.on_finalize()
    self.shutdown()
    return ret


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �������ʡ��Ǥ��� ExecutionContext ��
  #        ��ߤ��������Υ���ƥ�Ĥȶ��˽�λ������
  #
  # ���� RTC �������ʡ��Ǥ��뤹�٤Ƥμ¹ԥ���ƥ����Ȥ���ߤ��롣
  # ���� RTC ��¾�μ¹ԥ���ƥ����Ȥ��ͭ���� RTC ��°����¹ԥ���ƥ�����
  # (i.e. �¹ԥ���ƥ����Ȥ��ͭ���� RTC �Ϥ��ʤ�����μ¹ԥ���ƥ����Ȥ�
  # �����ʡ��Ǥ��롣)�˻��ä��Ƥ����硢���� RTC �Ϥ����Υ���ƥ����Ⱦ�
  # �������������ʤ���Фʤ�ʤ���
  # RTC ���¹���Τɤ� ExecutionContext �Ǥ� Active ���֤ǤϤʤ��ʤä��塢
  # ���� RTC �Ȥ���˴ޤޤ�� RTC ����λ���롣
  # 
  # ����
  # - RTC �����������Ƥ��ʤ���С���λ�����뤳�ȤϤǤ��ʤ���
  #   Created ���֤ˤ��� RTC �� exit() ��ƤӽФ�����硢
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Stop the RTC's execution context(s) and finalize it along with its
  #        contents.
  # 
  # Any execution contexts for which the RTC is the owner shall be stopped. 
  # If the RTC participates in any execution contexts belonging to another
  # RTC that contains it, directly or indirectly (i.e. the containing RTC
  # is the owner of the ExecutionContext), it shall be deactivated in those
  # contexts.
  # After the RTC is no longer Active in any Running execution context, it
  # and any RTCs contained transitively within it shall be finalized.
  #
  # Constraints
  # - An RTC cannot be exited if it has not yet been initialized. Any
  #   attempt to exit an RTC that is in the Created state shall fail with
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @return
  # 
  # @endif
  def exit(self):
    if self._created:
      return RTC.PRECONDITION_NOT_MET

    # deactivate myself on owned EC
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecMine,
                                        self.deactivate_comps(self._objref))
    # deactivate myself on other EC
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecOther,
                                        self.deactivate_comps(self._objref))

    # stop and detach myself from owned EC
    for ec in self._ecMine:
      ec.stop()
    #  ec.remove_component(self._this())

    # detach myself from other EC
    for ec in self._ecOther:
      # ec.stop()
      ec.remove_component(self._this())

    return self.finalize()


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �� Alive ���֤Ǥ��뤫�ɤ�����ǧ���롣
  #
  # RTC �����ꤷ�� ExecutionContext ���Ф��� Alive���֤Ǥ��뤫�ɤ�����ǧ���롣
  # RTC �ξ��֤� Active �Ǥ��뤫��Inactive �Ǥ��뤫��Error �Ǥ��뤫�ϼ¹����
  # ExecutionContext �˰�¸���롣���ʤ�������� ExecutionContext ���Ф��Ƥ�
  # Active  ���֤Ǥ��äƤ⡢¾�� ExecutionContext ���Ф��Ƥ� Inactive ���֤�
  # �ʤ���⤢�ꤨ�롣���äơ����Υ��ڥ졼�����ϻ��ꤵ�줿
  # ExecutionContext ���䤤��碌�ơ����� RTC �ξ��֤� Active��Inactive��
  # Error �ξ��ˤ� Alive ���֤Ȥ����֤���
  #
  # @param self
  #
  # @param exec_context �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return Alive ���ֳ�ǧ���
  #
  # @else
  #
  # @brief Confirm whether RTC is an Alive state or NOT.
  #
  # A component is alive or not regardless of the execution context from
  # which it is observed. However, whether or not it is Active, Inactive,
  # or in Error is dependent on the execution context(s) in which it is
  # running. That is, it may be Active in one context but Inactive in
  # another. Therefore, this operation shall report whether this RTC is
  # either Active, Inactive or in Error; which of those states a component
  # is in with respect to a particular context may be queried from the
  # context itself.
  #
  # @return Result of Alive state confirmation
  #
  # @endif
  def is_alive(self, exec_context):
    for ec in self._ecMine:
      if exec_context._is_equivalent(ec):
        return True

    for ec in self._ecOther:
      if exec_context._is_equivalent(ec):
        return True

    return False


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContextList���������
  #
  # ���� RTC ����ͭ���� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContextList.
  #
  # This operation returns a list of all execution contexts owned by this RTC.
  #
  # @return ExecutionContext List
  #
  # @endif
  #def get_contexts(self):
  #  execlist = []
  #  OpenRTM_aist.CORBA_SeqUtil.for_each(self._execContexts, self.ec_copy(execlist))
  #  return execlist


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext���������
  #
  # ���ꤷ���ϥ�ɥ�� ExecutionContext ��������롣
  # �ϥ�ɥ뤫�� ExecutionContext �ؤΥޥåԥ󥰤ϡ������ RTC ���󥹥��󥹤�
  # ��ͭ�Ǥ��롣�ϥ�ɥ�Ϥ��� RTC �� attach_context �����ݤ˼����Ǥ��롣
  #
  # @param self
  # @param ec_id �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return ExecutionContext
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContext.
  #
  # Obtain a reference to the execution context represented by the given 
  # handle.
  # The mapping from handle to context is specific to a particular RTC 
  # instance. The given handle must have been obtained by a previous call to 
  # attach_context on this RTC.
  #
  # @param ec_id ExecutionContext handle
  #
  # @return ExecutionContext
  #
  # @endif
  def get_context(self, ec_id):
    global ECOTHER_OFFSET

    # owned EC
    if ec_id < ECOTHER_OFFSET:
      if ec_id < len(self._ecMine):
        return self._ecMine[ec_id]
      else:
        return RTC.ExecutionContext._nil

    # participating EC
    index = ec_id - ECOTHER_OFFSET

    if index < len(self._ecOther):
      return self._ecOther[index]

    return RTC.ExecutionContext._nil


  ##
  # @if jp
  # @brief [CORBA interface] ��ͭ���� ExecutionContextList�� ��������
  #
  # ���� RTC ����ͭ���� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContextList.
  #
  # This operation returns a list of all execution contexts owned by this
  # RTC.
  #
  # @return ExecutionContext List
  #
  # @endif
  def get_owned_contexts(self):
    execlist = []
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecMine, self.ec_copy(execlist))
    
    return execlist # ExecutionContextList* 


  ##
  # @if jp
  # @brief [CORBA interface] ���ä��Ƥ��� ExecutionContextList ���������
  #
  # ���� RTC �����ä��Ƥ��� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get participating ExecutionContextList.
  #
  # This operation returns a list of all execution contexts in
  # which this RTC participates.
  #
  # @return ExecutionContext List
  #
  # @endif
  def get_participating_contexts(self):
    execlist = []
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecOther, self.ec_copy(execlist))
    
    return execlist # ExecutionContextList*


  #
  # @if jp
  # @brief [CORBA interface] ExecutionContext �Υϥ�ɥ���֤�
  #
  # @param ExecutionContext �¹ԥ���ƥ�����
  #
  # @return ExecutionContextHandle
  #
  # Ϳ����줿�¹ԥ���ƥ����Ȥ˴�Ϣ�դ���줿�ϥ�ɥ���֤���
  #
  # @else
  # @brief [CORBA interface] Return a handle of a ExecutionContext
  #
  # @param ExecutionContext
  #
  # @return ExecutionContextHandle
  #
  # This operation returns a handle that is associated with the given
  # execution context.
  #
  # @endif
  #
  def get_context_handle(self, cxt):
    # ec_id 0 : owned context
    # ec_id 1-: participating context
    if cxt._is_equivalent(self._ecMine[0]):
      return 0

    num = OpenRTM_aist.CORBA_SeqUtil.find(self._ecOther, self.ec_find(cxt))
    return num + 1 #ExecutionContextHandle_t


  #============================================================
  # RTC::RTObject
  #============================================================

  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] ����ݡ��ͥ�ȥץ��ե�������������
  #
  # ��������ݡ��ͥ�ȤΥץ��ե����������֤��� 
  #
  # @param self
  #
  # @return ����ݡ��ͥ�ȥץ��ե�����
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get RTC's profile
  #
  # This operation returns the ComponentProfile of the RTC
  #
  # @return ComponentProfile
  #
  # @endif
  def get_component_profile(self):
    try:
      return RTC.ComponentProfile(self._profile.instance_name,
                    self._profile.type_name,
                    self._profile.description,
                    self._profile.version,
                    self._profile.vendor,
                    self._profile.category,
                    self._portAdmin.getPortProfileList(),
                    self._profile.parent,
                    self._profile.properties)
    
    except:
      traceback.print_exception(*sys.exc_info())
    assert(False)
    return 0


  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] �ݡ��Ȥ��������
  #
  # ��������ݡ��ͥ�Ȥ���ͭ����ݡ��Ȥλ��Ȥ��֤���
  #
  # @param self
  #
  # @return �ݡ��ȥꥹ��
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get Ports
  #
  # This operation returns a list of the RTCs ports.
  #
  # @return PortList
  #
  # @endif
  def get_ports(self):
    try:
      return self._portAdmin.getPortServiceList()
    except:
      traceback.print_exception(*sys.exc_info())

    assert(False)
    return 0



  # RTC::ComponentAction

  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��attach����
  #
  # ���ꤷ�� ExecutionContext �ˤ��� RTC ���°�����롣���� RTC �ȴ�Ϣ���� 
  # ExecutionContext �Υϥ�ɥ���֤���
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::add_component ���ƤФ줿
  # �ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�����
  # ���Ƥ��ʤ���
  #
  # @param self
  # @param exec_context ��°�� ExecutionContext
  #
  # @return ExecutionContext �ϥ�ɥ�
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is participating in the given execution context. 
  # Return a handle that represents the association of this RTC with the 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::add_component. It is not intended for use by 
  # other clients.
  #
  # @param exec_context Prticipating ExecutionContext
  #
  # @return ExecutionContext Handle
  #
  # @endif
  def attach_context(self, exec_context):
    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    ecs = exec_context._narrow(RTC.ExecutionContextService)
    if CORBA.is_nil(ecs):
      return -1
    
    # if m_ecOther has nil element, insert attached ec to there.
    for i in range(len(self._ecOther)):
      if CORBA.is_nil(self._ecOther[i]):
        self._ecOther[i] = ecs
        return i + ECOTHER_OFFSET

    # no space in the list, push back ec to the last.
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._ecOther,ecs)
    
    return long(len(self._ecOther) - 1 + ECOTHER_OFFSET)


  def bindContext(self, exec_context):
    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    ecs = exec_context._narrow(RTC.ExecutionContextService)

    if CORBA.is_nil(ecs):
      return -1
    
    # if m_ecMine has nil element, insert attached ec to there.
    for i in range(len(self._ecMine)):
      if CORBA.is_nil(self._ecMine[i]):
        self._ecMine[i] = ecs
        return i + ECOTHER_OFFSET

    # no space in the list, push back ec to the last.
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._ecMine,ecs)
    
    return long(len(self._ecMine) - 1 + ECOTHER_OFFSET)


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��detach����
  #
  # ���ꤷ�� ExecutionContext ���餳�� RTC �ν�°�������롣
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::remove_component ���Ƥ�
  # �줿�ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�
  # ���ꤷ�Ƥ��ʤ���
  # 
  # ����
  # - ���ꤵ�줿 ExecutionContext �� RTC �����Ǥ˽�°���Ƥ��ʤ����ˤϡ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  # - ���ꤵ�줿 ExecutionContext �ˤ��������Ф��� RTC ��Active ���֤Ǥ����
  #   ��ˤϡ� ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param ec_id ����о� ExecutionContext�ϥ�ɥ�
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is no longer participating in the given execution 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::remove_component. It is not intended for use 
  # by other clients.
  # Constraints
  # - This operation may not be invoked if this RTC is not already 
  #   participating in the execution context. Such a call shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - This operation may not be invoked if this RTC is Active in the indicated
  #   execution context. Otherwise, it shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @param ec_id Dettaching ExecutionContext Handle
  #
  # @return
  #
  # @endif
  def detach_context(self, ec_id):
    _len = len(self._ecOther)

    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    if (long(ec_id) < long(ECOTHER_OFFSET)) or \
          (long(ec_id - ECOTHER_OFFSET) > _len):
      return RTC.BAD_PARAMETER
    
    index = long(ec_id - ECOTHER_OFFSET)

    if CORBA.is_nil(self._ecOther[index]):
      return RTC.BAD_PARAMETER
    
    OpenRTM_aist.CORBA_SeqUtil.erase(self._ecOther, index)

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν����
  #
  # RTC ����������졢Alive ���֤����ܤ��롣
  # RTC ��ͭ�ν���������Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onInitialize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Initialize RTC
  #
  # The RTC has been initialized and entered the Alive state.
  # Any RTC-specific initialization logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_initialize(self):
    ret = RTC.RTC_ERROR
    try:
      active_config = self._properties.getProperty("active_config")
      if ((active_config is None) or (active_config is "") or (active_config == [])):
        self._configsets.update("default")
      else:
        if self._configsets.haveConfig(active_config):
          self._configsets.update(active_config)
        else:
          self._configsets.update("default")
      ret = self.onInitialize()
    except:
      return RTC.RTC_ERROR

    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν�λ
  #
  # RTC ���˴�����롣
  # RTC ��ͭ�ν�λ�����Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onFinalize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Finalize RTC
  #
  # The RTC is being destroyed.
  # Any final RTC-specific tear-down logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_finalize(self):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onFinalize()
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ���
  #
  # RTC ����°���� ExecutionContext �� Stopped ���֤��� Running ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStartup() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] StartUp RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Stopped to Running.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_startup(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onStartup(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �����
  #
  # RTC ����°���� ExecutionContext �� Running ���֤��� Stopped ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onShutdown() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] ShutDown RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Running to Stopped.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_shutdown(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onShutdown(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ�����
  #
  # ��°���� ExecutionContext ���� RTC �����������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onActivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������ ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Activate RTC
  #
  # The RTC has been activated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_activated(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      self._configsets.update()
      ret = self.onActivated(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC ���������
  #
  # ��°���� ExecutionContext ���� RTC ������������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onDeactivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Deactivate RTC
  #
  # The RTC has been deactivated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_deactivated(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onDeactivated(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼���֤ؤ�����
  #
  # RTC ����°���� ExecutionContext �� Active ���֤��� Error ���֤����ܤ���
  # ���˸ƤӽФ���롣
  # ���Υ��ڥ졼������ RTC �� Error ���֤����ܤ����ݤ˰��٤����ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onAborting() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Transition Error State
  #
  # The RTC is transitioning from the Active state to the Error state in some
  # execution context.
  # This callback is invoked only a single time for time that the RTC 
  # transitions into the Error state from another state. This behavior is in 
  # contrast to that of on_error.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_aborting(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onAborting(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼����
  #
  # RTC �����顼���֤ˤ���ݤ˸ƤӽФ���롣
  # RTC �����顼���֤ξ��ˡ��оݤȤʤ� ExecutionContext ��ExecutionKind ��
  # �����������ߥ󥰤ǸƤӽФ���롣�㤨�С�
  # - ExecutionKind �� PERIODIC �ξ�硢�ܥ��ڥ졼������
  #   DataFlowComponentAction::on_execute �� on_state_update ���ؤ��ˡ�
  #   ���ꤵ�줿���֡����ꤵ�줿�����ǸƤӽФ���롣
  # - ExecutionKind �� EVENT_DRIVEN �ξ�硢�ܥ��ڥ졼������
  #   FsmParticipantAction::on_action ���ƤФ줿�ݤˡ��ؤ��˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onError() ������Хå��ؿ����Ƥӽ�
  # ����롣
  #
  # @param self
  # @param ec_id �о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Error Processing of RTC
  #
  # The RTC remains in the Error state.
  # If the RTC is in the Error state relative to some execution context when
  # it would otherwise be invoked from that context (according to the 
  # context��s ExecutionKind), this callback shall be invoked instead. 
  # For example,
  # - If the ExecutionKind is PERIODIC, this operation shall be invoked in 
  #   sorted order at the rate of the context instead of 
  #   DataFlowComponentAction::on_execute and on_state_update.
  # - If the ExecutionKind is EVENT_DRIVEN, this operation shall be invoked 
  #   whenever FsmParticipantAction::on_action would otherwise have been 
  #   invoked.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_error(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onError(ec_id)
      self._configsets.update()
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υꥻ�å�
  #
  # Error ���֤ˤ��� RTC �Υꥫ�Х������¹Ԥ���Inactive ���֤�����������
  # ���˸ƤӽФ���롣
  # RTC �Υꥫ�Х������������������ Inactive ���֤��������뤬������ʳ���
  # ���ˤ� Error ���֤�α�ޤ롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onReset() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # @param self
  # @param ec_id �ꥻ�å��о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Resetting RTC
  #
  # The RTC is in the Error state. An attempt is being made to recover it such
  # that it can return to the Inactive state.
  # If the RTC was successfully recovered and can safely return to the
  # Inactive state, this method shall complete with ReturnCode_t::OK. Any
  # other result shall indicate that the RTC should remain in the Error state.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_reset(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onReset(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ���������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onExecute() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Primary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the first execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_execute(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onExecute(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(�������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ����������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStateUpdate() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Secondary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the second execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_state_update(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onStateUpdate(ec_id)
      self._configsets.update()
    except:
      return RTC.RTC_ERROR
    
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] �¹Լ����ѹ�����
  #
  # �ܥ��ڥ졼�����ϡ�ExecutionContext �μ¹Լ������ѹ����줿���Ȥ����Τ���
  # �ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onRateChanged() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Notify rate chenged
  #
  # This operation is a notification that the rate of the indicated execution 
  # context has changed.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_rate_changed(self, ec_id):
    ret = RTC.RTC_ERROR
    try:
      ret = self.onRateChanged(ec_id)
    except:
      return RTC.RTC_ERROR
    
    return ret


  #============================================================
  # SDOPackage::SdoSystemElement
  #============================================================

  ##
  # @if jp
  # 
  # @brief [SDO interface] Organization �ꥹ�Ȥμ��� 
  #
  # SDOSystemElement ��0�Ĥ⤷���Ϥ���ʾ�� Organization ���ͭ���뤳�Ȥ�
  # ����롣 SDOSystemElement ��1�İʾ�� Organization ���ͭ���Ƥ�����
  # �ˤϡ����Υ��ڥ졼�����Ͻ�ͭ���� Organization �Υꥹ�Ȥ��֤���
  # �⤷Organization���Ĥ��ͭ���Ƥ��ʤ�����ж��Υꥹ�Ȥ��֤���
  #
  # @param self
  #
  # @return ��ͭ���Ƥ��� Organization �ꥹ��
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # SDOSystemElement can be the owner of zero or more organizations.
  # If the SDOSystemElement owns one or more Organizations, this operation
  # returns the list of Organizations that the SDOSystemElement owns.
  # If it does not own any Organization, it returns empty list.
  #
  # @return Owned Organization List
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_owned_organizations(self):
    try:
      return self._sdoOwnedOrganizations
    except:
      raise SDOPackage.NotAvailable

    return []


  #============================================================
  # SDOPackage::SDO
  #============================================================

  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO ID �μ���
  #
  # SDO ID ���֤����ڥ졼�����
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  # 
  # @return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� ID
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO ID
  #
  # This operation returns id of the SDO.
  # This operation throws SDOException with one of the following types.
  #
  # @return    id of the SDO defined in the resource data model.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_sdo_id(self):
    try:
      return self._profile.instance_name
    except:
      raise SDOPackage.InternalError("get_sdo_id()")


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO �����פμ���
  # 
  # SDO Type ���֤����ڥ졼�����
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  #
  # @return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� Type
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO type
  #
  # This operation returns sdoType of the SDO.
  # This operation throws SDOException with one of the following types.
  #
  # @return    Type of the SDO defined in the resource data model.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_sdo_type(self):
    try:
      return self._profile.description
    except:
      raise SDOPackage.InternalError("get_sdo_type()")
    return ""


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO DeviceProfile �ꥹ�Ȥμ��� 
  #
  # SDO �� DeviceProfile ���֤����ڥ졼����� SDO ���ϡ��ɥ������ǥХ���
  # �˴�Ϣ�դ����Ƥ��ʤ����ˤϡ����� DeviceProfile ���֤���롣
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  #
  # @return    SDO DeviceProfile
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO DeviceProfile
  #
  # This operation returns the DeviceProfile of the SDO. If the SDO does not
  # represent any hardware device, then a DeviceProfile with empty values
  # are returned.
  # This operation throws SDOException with one of the following types.
  #
  # @return    The DeviceProfile of the SDO.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_device_profile(self):
    try:
      dprofile = SDOPackage.DeviceProfile(self._SdoConfigImpl.device_type,
                                          self._SdoConfigImpl.manufacturer,
                                          self._SdoConfigImpl.model,
                                          self._SdoConfigImpl.version,
                                          self._SdoConfigImpl.properties)
      return dprofile
    except:
      raise SDOPackage.InternalError("get_device_profile()")

    return SDOPackage.DeviceProfile("","","","",[])


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO ServiceProfile �μ��� 
  #
  # SDO ����ͭ���Ƥ��� Service �� ServiceProfile ���֤����ڥ졼�����
  # SDO �������ӥ����Ĥ��ͭ���Ƥ��ʤ����ˤϡ����Υꥹ�Ȥ��֤���
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  # 
  # @return    SDO ���󶡤������Ƥ� Service �� ServiceProfile��
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO ServiceProfile
  # 
  # This operation returns a list of ServiceProfiles that the SDO has.
  # If the SDO does not provide any service, then an empty list is returned.
  # This operation throws SDOException with one of the following types.
  # 
  # @return    List of ServiceProfiles of all the services the SDO is
  #            providing.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_service_profiles(self):
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()
    try:
      return self._sdoSvcProfiles
    except:
      raise SDOPackage.InternalError("get_service_profiles()")

    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] �����ServiceProfile�μ��� 
  #
  # ���� "id" �ǻ��ꤵ�줿̾���Υ����ӥ��� ServiceProfile ���֤���
  # 
  # @param     self
  # @param     _id SDO Service �� ServiceProfile �˴�Ϣ�դ���줿���̻ҡ�
  # 
  # @return    ���ꤵ�줿 SDO Service �� ServiceProfile��
  # 
  # @exception InvalidParameter "id" �ǻ��ꤷ�� ServiceProfile ��¸�ߤ��ʤ���
  #                             "id" �� null��
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # This operation returns the ServiceProfile that is specified by the
  # argument "id."
  # 
  # @param     _id The identifier referring to one of the ServiceProfiles.
  # 
  # @return    The profile of the specified service.
  # 
  # @exception InvalidParameter if the ServiceProfile that is specified by 
  #                             the argument 'id' does not exist or if 'id'
  #                             is 'null.'
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable If the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError If the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_service_profile(self, _id):
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()
    if not _id:
      raise SDOPackage.InvalidParameter("get_service_profile(): Empty name.")

    try:
      index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

      if index < 0:
        raise SDOPackage.InvalidParameter("get_service_profile(): Not found")

      return self._sdoSvcProfiles[index]
    except:
      raise SDOPackage.InternalError("get_service_profile()")

    return SDOPackage.ServiceProfile("", "", [], None)


  ##
  # @if jp
  # 
  # @brief [SDO interface] ���ꤵ�줿 SDO Service �μ���
  #
  # ���Υ��ڥ졼�����ϰ��� "id" �ǻ��ꤵ�줿̾���ˤ�äƶ��̤����
  # SDO �� Service �ؤΥ��֥������Ȼ��Ȥ��֤��� SDO �ˤ���󶡤����
  # Service �Ϥ��줾���դμ��̻Ҥˤ����̤���롣
  #
  # @param self
  # @param _id SDO Service �˴�Ϣ�դ���줿���̻ҡ�
  #
  # @return �׵ᤵ�줿 SDO Service �ؤλ��ȡ�
  #
  # 
  # @exception InvalidParameter "id" �ǻ��ꤷ�� ServiceProfile ��¸�ߤ��ʤ���
  #                             "id" �� null��
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting specified SDO Service's reference
  #
  # This operation returns an object implementing an SDO's service that
  # is identified by the identifier specified as an argument. Different
  # services provided by an SDO are distinguished with different
  # identifiers. See OMG SDO specification Section 2.2.8, "ServiceProfile,"
  # on page 2-12 for more details.
  #
  # @param _id The identifier referring to one of the SDO Service
  # @return The object implementing the requested service.
  # @exception InvalidParameter if argument ��id�� is null, or if the 
  #                             ServiceProfile that is specified by argument
  #                            ��id�� does not exist.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable If the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError If the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_sdo_service(self, _id):
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()

    if not _id:
      raise SDOPackage.InvalidParameter("get_service(): Empty name.")

    try:
      index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

      if index < 0:
        raise SDOPackage.InvalidParameter("get_service(): Not found")

      return self._sdoSvcProfiles[index].service
    except:
      raise SDOPackage.InternalError("get_service()")
    return SDOPackage.SDOService._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Configuration ���֥������Ȥμ��� 
  #
  # ���Υ��ڥ졼������ Configuration interface �ؤλ��Ȥ��֤���
  # Configuration interface �ϳ� SDO ��������뤿��Υ��󥿡��ե�������
  # �ҤȤĤǤ��롣���Υ��󥿡��ե������� DeviceProfile, ServiceProfile,
  # Organization ��������줿 SDO ��°���ͤ����ꤹ�뤿��˻��Ѥ���롣
  # Configuration ���󥿡��ե������ξܺ٤ˤĤ��Ƥϡ�OMG SDO specification
  # �� 2.3.5��, p.2-24 �򻲾ȤΤ��ȡ�
  #
  # @param self
  #
  # @return SDO �� Configuration ���󥿡��ե������ؤλ���
  #
  # @exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
  #                                    �����ʤ���
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Configuration object
  #
  # This operation returns an object implementing the Configuration
  # interface. The Configuration interface is one of the interfaces that
  # each SDO maintains. The interface is used to configure the attributes
  # defined in DeviceProfile, ServiceProfile, and Organization.
  # See OMG SDO specification Section 2.3.5, "Configuration Interface,"
  # on page 2-24 for more details about the Configuration interface.
  #
  # @return The Configuration interface of an SDO.
  #
  # @exception InterfaceNotImplemented The target SDO has no Configuration
  #                                    interface.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration(self):
    if self._SdoConfig is None:
      raise SODPackage.InterfaceNotImplemented()
    try:
      return self._SdoConfig
    except:
      raise SDOPackage.InternalError("get_configuration()")
    return SDOPackage.Configuration._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Monitoring ���֥������Ȥμ��� 
  #
  # ���Υ��ڥ졼������ Monitoring interface �ؤλ��Ȥ��֤���
  # Monitoring interface �� SDO ���������륤�󥿡��ե������ΰ�ĤǤ��롣
  # ���Υ��󥿡��ե������� SDO �Υץ��ѥƥ����˥���󥰤��뤿���
  # ���Ѥ���롣
  # Monitoring interface �ξܺ٤ˤĤ��Ƥ� OMG SDO specification ��
  # 2.3.7�� "Monitoring Interface" p.2-35 �򻲾ȤΤ��ȡ�
  #
  # @param self
  #
  # @return SDO �� Monitoring interface �ؤλ���
  #
  # @exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
  #                                    �����ʤ���
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Get Monitoring object
  #
  # This operation returns an object implementing the Monitoring interface.
  # The Monitoring interface is one of the interfaces that each SDO
  # maintains. The interface is used to monitor the properties of an SDO.
  # See OMG SDO specification Section 2.3.7, "Monitoring Interface," on
  # page 2-35 for more details about the Monitoring interface.
  #
  # @return The Monitoring interface of an SDO.
  #
  # @exception InterfaceNotImplemented The target SDO has no Configuration
  #                                    interface.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_monitoring(self):
    raise SDOPackage.InterfaceNotImplemented("Exception: get_monitoring")
    return SDOPackage.Monitoring._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Organization �ꥹ�Ȥμ��� 
  #
  # SDO ��0�İʾ�� Organization (�ȿ�)�˽�°���뤳�Ȥ��Ǥ��롣 �⤷ SDO ��
  # 1�İʾ�� Organization �˽�°���Ƥ����硢���Υ��ڥ졼�����Ͻ�°����
  # Organization �Υꥹ�Ȥ��֤���SDO �� �ɤ� Organization �ˤ��°���Ƥ��ʤ�
  # ���ˤϡ����Υꥹ�Ȥ��֤���롣
  #
  # @param self
  #
  # @return SDO ����°���� Organization �Υꥹ�ȡ�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # An SDO belongs to zero or more organizations. If the SDO belongs to one
  # or more organizations, this operation returns the list of organizations
  # that the SDO belongs to. An empty list is returned if the SDO does not
  # belong to any Organizations.
  #
  # @return The list of Organizations that the SDO belong to.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_organizations(self):
    self._sdoOrganizations = self._SdoConfigImpl.getOrganizations()
    try:
      return self._sdoOrganizations
    except:
      raise SDOPackage.InternalError("get_organizations()")
    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO Status �ꥹ�Ȥμ��� 
  #
  # ���Υ��ڥ졼������ SDO �Υ��ơ�������ɽ�� NVList ���֤���
  #
  # @param self
  #
  # @return SDO �Υ��ơ�������
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Get SDO Status
  #
  # This operation returns an NVlist describing the status of an SDO.
  #
  # @return The actual status of an SDO.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  def get_status_list(self):
    try:
      return self._sdoStatus
    except:
      raise SDOPackage.InternalError("get_status_list()")
    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO Status �μ��� 
  #
  # This operation returns the value of the specified status parameter.
  #
  # @param self
  # @param name SDO �Υ��ơ��������������ѥ�᡼����
  # 
  # @return ���ꤵ�줿�ѥ�᡼���Υ��ơ������͡�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InvalidParameter ���� "name" �� null ���뤤��¸�ߤ��ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [SDO interface] Get SDO Status
  #
  # @param name One of the parameters defining the "status" of an SDO.
  #
  # @return The value of the specified status parameter.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The parameter defined by "name" is null or
  #                             does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  #
  # @endif
  def get_status(self, name):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoStatus, self.nv_name(name))
    if index < 0:
      raise SDOPackage.InvalidParameter("get_status(): Not found")

    try:
      return any.to_any(self._sdoStatus[index].value)
    except:
      raise SDOPackage.InternalError("get_status()")
    return any.to_any("")


  #============================================================
  # Local interfaces
  #============================================================

  ##
  # @if jp
  #
  # @brief [local interface] ���󥹥���̾�μ���
  # 
  # ComponentProfile �����ꤵ�줿���󥹥���̾���֤���
  #
  # @param self
  # 
  # @return ���󥹥���̾
  # 
  # @else
  # 
  # @endif
  def getInstanceName(self):
    return self._profile.instance_name


  ##
  # @if jp
  #
  # @brief [local interface] ���󥹥���̾������
  # 
  # ComponentProfile �˻��ꤵ�줿���󥹥���̾�����ꤹ�롣
  #
  # @param self
  # 
  # @param instance_name ���󥹥���̾
  # 
  # @else
  # 
  # @endif
  def setInstanceName(self, instance_name):
    self._properties.setProperty("instance_name",instance_name)
    self._profile.instance_name = self._properties.getProperty("instance_name")


  ##
  # @if jp
  #
  # @brief [local interface] ��̾�μ���
  # 
  # ComponentProfile �����ꤵ�줿��̾���֤���
  #
  # @param self
  # 
  # @return ��̾
  # 
  # @else
  # 
  # @endif
  def getTypeName(self):
    return self._profile.type_name


  ##
  # @if jp
  #
  # @brief [local interface] Description �μ���
  # 
  # ComponentProfile �����ꤵ�줿 Description ���֤���
  #
  # @param self
  # 
  # @return Description
  # 
  # @else
  # 
  # @endif
  def getDescription(self):
    return self._profile.description


  ##
  # @if jp
  #
  # @brief [local interface] �С���������μ���
  # 
  # ComponentProfile �����ꤵ�줿�С�����������֤���
  #
  # @param self
  # 
  # @return �С���������
  # 
  # @else
  # 
  # @endif
  def getVersion(self):
    return self._profile.version


  ##
  # @if jp
  #
  # @brief [local interface] �٥��������μ���
  # 
  # ComponentProfile �����ꤵ�줿�٥����������֤���
  #
  # @param self
  # 
  # @return �٥��������
  # 
  # @else
  # 
  # @endif
  def getVendor(self):
    return self._profile.vendor


  ##
  # @if jp
  #
  # @brief [local interface] ���ƥ������μ���
  # 
  # ComponentProfile �����ꤵ�줿���ƥ��������֤���
  #
  # @param self
  # 
  # @return ���ƥ������
  # 
  # @else
  # 
  # @endif
  def getCategory(self):
    return self._profile.category


  ##
  # @if jp
  #
  # @brief [local interface] Naming Server ����μ���
  # 
  # ���ꤵ�줿 Naming Server ������֤���
  #
  # @param self
  # 
  # @return Naming Server �ꥹ��
  # 
  # @else
  # 
  # @endif
  def getNamingNames(self):
    return string.split(self._properties.getProperty("naming.names"), ",")


  ##
  # @if jp
  #
  # @brief [local interface] ���֥������ȥ�ե���󥹤�����
  # 
  # RTC �� CORBA ���֥������ȥ�ե���󥹤����ꤹ�롣
  # 
  # @param self
  # @param rtobj ���֥������ȥ�ե����
  # 
  # @else
  # 
  # @endif
  def setObjRef(self, rtobj):
    self._objref = rtobj
    return


  ##
  # @if jp
  #
  # @brief [local interface] ���֥������ȥ�ե���󥹤μ���
  # 
  # ���ꤵ�줿 CORBA ���֥������ȥ�ե���󥹤�������롣
  # 
  # @param self
  # 
  # @return ���֥������ȥ�ե����
  # 
  # @else
  # 
  # @endif
  def getObjRef(self):
    return self._objref


  ##
  # @if jp
  # 
  # @brief [local interface] RTC �Υץ��ѥƥ������ꤹ��
  #
  # RTC ���ݻ����٤��ץ��ѥƥ������ꤹ�롣Ϳ������ץ��ѥƥ��ϡ�
  # ComponentProfile �������ꤵ���٤����������ʤ���Фʤ�ʤ���
  # ���Υ��ڥ졼�������̾� RTC ������������ݤ� Manager ����
  # �ƤФ�뤳�Ȥ�տޤ��Ƥ��롣
  # 
  # @param self
  # @param prop RTC �Υץ��ѥƥ�
  #
  # @else
  #
  # @brief [local interface] Set RTC property
  #
  # This operation sets the properties to the RTC. The given property
  # values should include information for ComponentProfile.
  # Generally, this operation is designed to be called from Manager, when
  # RTC is initialized
  #
  # @param prop Property for RTC.
  #
  # @endif
  def setProperties(self, prop):
    self._properties = self._properties.mergeProperties(prop)
    self._profile.instance_name = self._properties.getProperty("instance_name")
    self._profile.type_name     = self._properties.getProperty("type_name")
    self._profile.description   = self._properties.getProperty("description")
    self._profile.version       = self._properties.getProperty("version")
    self._profile.vendor        = self._properties.getProperty("vendor")
    self._profile.category      = self._properties.getProperty("category")


  ##
  # @if jp
  # 
  # @brief [local interface] RTC �Υץ��ѥƥ����������
  #
  # RTC ���ݻ����Ƥ���ץ��ѥƥ����֤���
  # RTC���ץ��ѥƥ�������ʤ����϶��Υץ��ѥƥ����֤���롣
  # 
  # @param self
  # 
  # @return RTC �Υץ��ѥƥ�
  #
  # @else
  #
  # @brief [local interface] Get RTC property
  #
  # This operation returns the properties of the RTC.
  # Empty property would be returned, if RTC has no property.
  #
  # @return Property for RTC.
  #
  # @endif
  def getProperties(self):
    return self._properties


  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼��������
  # 
  # ����ե�����졼�����ѥ�᡼�����ѿ���Х���ɤ���
  # \<VarType\>�Ȥ��ƥ���ե�����졼�����ѥ�᡼���Υǡ���������ꤹ�롣
  #
  # @param self
  # @param param_name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ����ե�����졼�����ѥ�᡼���ǥե������
  # @param trans ʸ�����Ѵ��Ѵؿ�(�ǥե������:None)
  #
  # @return ������(��������:true�����꼺��:false)
  # 
  # @else
  #
  # @endif
  def bindParameter(self, param_name, var,
                    def_val, trans=None):
    if trans is None:
      _trans = OpenRTM_aist.stringTo
    else:
      _trans = trans
    self._configsets.bindParameter(param_name, var, def_val, _trans)
    return True


  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(ID����)
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ����ꤷ���ͤǡ�
  # ����ե�����졼�����ѥ�᡼�����ͤ򹹿�����
  #
  # @param self
  # @param config_set �����оݤΥ���ե�����졼����󥻥å�ID
  # 
  # @else
  #
  # @endif
  def updateParameters(self, config_set):
    self._configsets.update(config_set)
    return


  ##
  # @if jp
  # 
  # @brief [local interface] Port ����Ͽ����
  #
  # RTC ���ݻ�����Port����Ͽ���롣
  # Port �������饢��������ǽ�ˤ��뤿��ˤϡ����Υ��ڥ졼�����ˤ��
  # ��Ͽ����Ƥ��ʤ���Фʤ�ʤ�����Ͽ����� Port �Ϥ��� RTC �����ˤ�����
  # PortProfile.name �ˤ����̤���롣�������äơ�Port �� RTC ��ˤ����ơ�
  # ��ˡ����� PortProfile.name ������ʤ���Фʤ�ʤ���
  # ��Ͽ���줿 Port ��������Ŭ�ڤ˥����ƥ��ֲ����줿�塢���λ��Ȥ�
  # ���֥������Ȼ��Ȥ��ꥹ�������¸����롣
  # 
  # @param self
  # @param port RTC ����Ͽ���� Port
  # @param port_type if port is PortBase, port_type is None,
  #                  if port is PortService, port_type is True
  #
  # @else
  #
  # @brief [local interface] Register Port
  #
  # This operation registers a Port to be held by this RTC.
  # In order to enable access to the Port from outside of RTC, the Port
  # must be registered by this operation. The Port that is registered by
  # this operation would be identified by PortProfile.name in the inside of
  # RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
  # The registering Port would be activated properly, and the reference
  # and the object reference would be stored in lists in RTC.
  #
  # @param port Port which is registered in the RTC
  #
  # @endif
  def registerPort(self, port, port_type=None):
    self._portAdmin.registerPort(port)
    if port_type is not None:
      port.setOwner(self.getObjRef())
    return


  ##
  # @if jp
  # 
  # @brief [local interface] DataInPort ����Ͽ����
  #
  # RTC ���ݻ����� DataInPort ����Ͽ���롣
  # Port �Υץ��ѥƥ��˥ǡ����ݡ��ȤǤ��뤳��("port.dataport")��
  # TCP����Ѥ��뤳��("tcp_any")�����ꤹ��ȤȤ�ˡ� DataInPort ��
  # ���󥹥��󥹤�����������Ͽ���롣
  # 
  # @param self
  # @param name port ̾��
  # @param inport ��Ͽ�о� DataInPort
  #
  # @else
  #
  # @endif
  def registerInPort(self, name, inport):
    propkey = "port.dataport."
    propkey += name
    propkey += ".tcp_any"
    self._properties.setProperty(propkey,self._properties.getProperty(propkey))
    port = OpenRTM_aist.DataInPort(name, inport, self._properties.getNode(propkey))
    self.registerPort(port)
    return


  ##
  # @if jp
  # 
  # @brief [local interface] DataOutPort ����Ͽ����
  #
  # RTC ���ݻ����� DataOutPor t����Ͽ���롣
  # Port �Υץ��ѥƥ��˥ǡ����ݡ��ȤǤ��뤳��("port.dataport")��
  # TCP����Ѥ��뤳��("tcp_any")�����ꤹ��ȤȤ�ˡ� DataOutPort ��
  # ���󥹥��󥹤�����������Ͽ���롣
  # 
  # @param self
  # @param name port ̾��
  # @param outport ��Ͽ�о� DataInPort
  #
  # @else
  #
  # @endif
  def registerOutPort(self, name, outport):
    propkey = "port.dataport."
    propkey += name
    propkey += ".tcp_any"
    self._properties.setProperty(propkey,self._properties.getProperty(propkey))
    port = OpenRTM_aist.DataOutPort(name, outport, self._properties.getNode(propkey))
    self.registerPort(port)
    return


  ##
  # @if jp
  # 
  # @brief [local interface] Port ����Ͽ��������
  #
  # RTC ���ݻ�����Port����Ͽ�������롣
  # 
  # @param self
  # @param port ����о� Port
  #
  # @else
  #
  # @brief [local interface] Unregister Port
  #
  # This operation unregisters a Port to be held by this RTC.
  #
  # @param port Port which is unregistered in the RTC
  #
  # @endif
  def deletePort(self, port):
    self._portAdmin.deletePort(port)
    return


  ##
  # @if jp
  # 
  # @brief [local interface] ̾������ˤ�� Port ����Ͽ��������
  #
  # ̾�Τ���ꤷ�� RTC ���ݻ�����Port����Ͽ�������롣
  # 
  # @param self
  # @param port_name ����о� Port ̾
  #
  # @else
  #
  # @endif
  def deletePortByName(self, port_name):
    self._portAdmin.deletePortByName(port_name)
    return


  ##
  # @if jp
  #
  # @brief �� Port ����Ͽ��������
  #
  # RTC ���ݻ��������Ƥ� Port �������롣
  # 
  # @param self
  #
  # @else
  #
  # @brief Unregister the All Portse
  #
  # This operation deactivates the all Port and deletes the all Port's
  # registrations in the RTC..
  #
  # @endif
  def finalizePorts(self):
    self._portAdmin.finalizePorts()
    return


  ##
  # @if jp
  #
  # @brief RTC ��λ����
  #
  # RTC �ν�λ������¹Ԥ��롣
  # �ݻ����Ƥ����� Port ����Ͽ��������ȤȤ�ˡ��������� CORBA ���֥�������
  # �������������RTC ��λ���롣
  # 
  # @param self
  #
  # @else
  #
  # @endif
  def shutdown(self):
    try:
      self.finalizePorts()
      self._poa.deactivate_object(self._poa.servant_to_id(self._SdoConfigImpl))
      self._poa.deactivate_object(self._poa.servant_to_id(self))
    except:
      traceback.print_exception(*sys.exc_info())

    if self._manager:
      self._manager.cleanupComponent(self)
      
    return



  ##
  # @if jp
  # @class svc_name
  # @brief SDOService �Υץ��ե�����ꥹ�Ȥ���id�ǥ��������뤿���
  # �ե��󥯥����饹
  # @else
  #
  # @endif
  class svc_name:
    def __init__(self, _id):
      self._id= _id

    def __call__(self, prof):
      return self._id == prof.id


  #------------------------------------------------------------
  # Functor
  #------------------------------------------------------------

  ##
  # @if jp
  # @class nv_name
  # @brief NVList �����ѥե��󥯥�
  # @else
  #
  # @endif
  class nv_name:
    def __init__(self, _name):
      self._name = _name

    def __call__(self, nv):
      return self._name == nv.name


  ##
  # @if jp
  # @class ec_find
  # @brief ExecutionContext �����ѥե��󥯥�
  # @else
  #
  # @endif
  class ec_find:
    def __init__(self, ec):
      self._ec = _ec

    def __call__(self, ecs):
      try:
        ec = ecs._narrow(RTC.ExecutionContext)
        return self._ec._is_equivalent(ec)
      except:
        return False

      return False


  ##
  # @if jp
  # @class ec_copy
  # @brief ExecutionContext Copy�ѥե��󥯥�
  # @else
  #
  # @endif
  class ec_copy:
    def __init__(self, eclist):
      self._eclist = eclist

    def __call__(self, ecs):
      self._eclist.append(ecs)


  ##
  # @if jp
  # @class deactivate_comps
  # @brief RTC ��������ѥե��󥯥�
  # @else
  #
  # @endif
  class deactivate_comps:
    def __init__(self, comp):
      self._comp = comp

    def __call__(self, ec):
      ec.deactivate_component(self._comp)


# RtcBase = RTObject_impl
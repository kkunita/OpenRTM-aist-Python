#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# \file DefaultConfiguration.py
# \brief RTC manager default configuration
# \date $Date: $
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import OpenRTM_aist
import platform


if platform.system() == "Windows":
    cpp_suffixes = "dll"
elif platform.system() == "Linux":
    cpp_suffixes = "so"
else:
    cpp_suffixes = "dylib"

##
# @if jp
# @brief Manager 用 デフォルト・コンフィギュレーション
#
# Managerクラス用デフォルトコンフィギュレーション。
#
# @since 0.4.0
#
# @else
# @endif
default_config =["config.version",                   OpenRTM_aist.openrtm_version,
                 "openrtm.name",                     OpenRTM_aist.openrtm_name,
                 "openrtm.version",                  OpenRTM_aist.openrtm_version,
                 "manager.instance_name",            "manager",
                 "manager.name",                     "manager",
                 "manager.naming_formats",           "%h.host_cxt/%n.mgr",
                 "manager.pid",                      "",
                 "os.name",                          "",
                 "os.release",                       "",
                 "os.version",                       "",
                 "os.arch",                          "",
                 "os.hostname",                      "",
                 "logger.enable",                    "YES",
                 "logger.file_name",                 "./rtc%p.log",
                 "logger.date_format",               "%b %d %H:%M:%S",
                 "logger.log_level",                 "INFO",
                 "logger.stream_lock",               "NO",
                 "logger.master_logger",             "",
                 "module.conf_path",                 "",
                 "module.load_path",                 "",
                 "naming.enable",                    "YES",
                 "naming.type",                      "corba",
                 "naming.formats",                   "%h.host_cxt/%n.rtc",
                 "naming.update.enable",             "YES",
                 "naming.update.interval",           "10.0",
                 "timer.enable",                     "YES",
                 "timer.tick",                       "0.1",
                 "corba.args",                       "",
                 "corba.endpoints",                   "",
                 "corba.id",                         OpenRTM_aist.corba_name,
                 "corba.nameservers",               "localhost",
                 "corba.master_manager",             "localhost:2810",
                 "corba.nameservice.replace_endpoint", "NO",
                 "corba.update_master_manager.enable", "YES",
                 "corba.update_master_manager.interval", "10.0",
                 "exec_cxt.periodic.type",           "PeriodicExecutionContext",
                 "exec_cxt.periodic.rate",           "1000",
                 "exec_cxt.sync_transition",         "YES",
                 "exec_cxt.transition_timeout",      "0.5",
                 "manager.modules.load_path",        "./",
                 "manager.modules.abs_path_allowed", "YES",
                 "manager.is_master",                "NO",
                 "manager.corba_servant",            "YES",
                 "manager.shutdown_on_nortcs",       "YES",
                 "manager.shutdown_auto",            "YES",
                 "manager.auto_shutdown_duration",   "10.0",
                 "manager.name",                     "manager",
                 "manager.command",                  "rtcd",
                 "manager.nameservers",               "default",
                 "manager.language",                 "Python",
                 "manager.components.naming_policy", "process_unique",
                 "manager.modules.C++.manager_cmd", "rtcd",
                 "manager.modules.Python.manager_cmd", "rtcd_python",
                 "manager.modules.Java.manager_cmd", "rtcd_java",
                 "manager.modules.search_auto", "YES",
                 "manager.local_service.enabled_services","ALL",
                 "sdo.service.provider.enabled_services",  "ALL",
                 "sdo.service.consumer.enabled_services",  "ALL",
                 "manager.supported_languages",  "C++, Python, Java",
                 "manager.modules.C++.profile_cmd",  "rtcprof",
                 "manager.modules.Python.profile_cmd",  "rtcprof_python",
                 "manager.modules.Java.profile_cmd",  "rtcprof_java",
                 "manager.modules.C++.suffixes",  cpp_suffixes,
                 "manager.modules.Python.suffixes",  "py",
                 "manager.modules.Java.suffixes",  "class",
                 "manager.modules.C++.load_paths",  "./",
                 "manager.modules.Python.load_paths",  "./",
                 "manager.modules.Java.load_paths",  "./",
                 ""]

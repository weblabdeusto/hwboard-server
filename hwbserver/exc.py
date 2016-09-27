#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
#
import weblab.experiment.exc as ExperimentErrors



# New exceptions (updated for the 2016 version of the experiment server)

class ConfigurationError(ExperimentErrors.ExperimentError):
    """
    To be raised when an important configuration variable is missing or is improperly configured.
    """
    def __init__(self,*args,**kwargs):
        ExperimentErrors.ExperimentError.__init__(self,*args,**kwargs)

class DeviceServerError(ExperimentErrors.ExperimentError):
    """
    To be raised when there is any kind of device-server related error (such as no connection to the device server).
    """
    def __init__(self,*args,**kwargs):
        ExperimentErrors.ExperimentError.__init__(self,*args,**kwargs)

class UnhandledExceptionError(ExperimentErrors.ExperimentError):
    """
    To be raised when an exception that we do NOT expect is raised.
    """
    def __init__(self,*args,**kwargs):
        ExperimentErrors.ExperimentError.__init__(self,*args,**kwargs)

# Old exceptions (may be used or not)

class UdXilinxExperimentError(ExperimentErrors.ExperimentError):
    def __init__(self,*args,**kargs):
        ExperimentErrors.ExperimentError.__init__(self,*args,**kargs)

class UdBoardCommandError(UdXilinxExperimentError):
    def __init__(self, *args, **kargs):
        UdXilinxExperimentError.__init__(self, *args, **kargs)

class InvalidUdBoardCommandError(UdBoardCommandError):
    def __init__(self, *args, **kargs):
        UdBoardCommandError.__init__(self, *args, **kargs)

class IllegalStatusUdBoardCommandError(UdBoardCommandError):
    def __init__(self, *args, **kargs):
        UdBoardCommandError.__init__(self, *args, **kargs)

class InvalidDeviceToProgramError(UdBoardCommandError):
    def __init__(self, *args, **kargs):
        UdBoardCommandError.__init__(self, *args, **kargs)

class InvalidDeviceToSendCommandsError(UdBoardCommandError):
    def __init__(self, *args, **kargs):
        UdBoardCommandError.__init__(self, *args, **kargs)

class InvalidXilinxDeviceError(UdBoardCommandError):
    def __init__(self, *args, **kargs):
        UdBoardCommandError.__init__(self, *args, **kargs)
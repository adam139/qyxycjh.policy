#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from qyxycjh.policy import _

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

#文件夹mark interfaces,用于定义视图
# todo :定义db_ajax_listing view
class IAixinjuankuan (Interface):
    """某一捐赠项目具体捐赠记录"""
class IJuanzenggongshi (Interface):
    """展示已有捐赠的项目"""

class IContainerTablelist (Interface):
    """文件夹标记接口"""


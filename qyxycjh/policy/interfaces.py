#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from qyxycjh.policy import _

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """
class ICreateOrgEvent(Interface):
    """新增一个organization object"""


class IContainerTablelist (Interface):
    """文件夹标记接口"""


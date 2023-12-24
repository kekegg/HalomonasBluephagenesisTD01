#
# Autogenerated by Thrift Compiler (0.15.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class mapOptions(object):
    """
    Attributes:
     - zoomScale
     - ifReverse

    """


    def __init__(self, zoomScale=None, ifReverse=None,):
        self.zoomScale = zoomScale
        self.ifReverse = ifReverse

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.DOUBLE:
                    self.zoomScale = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.ifReverse = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('mapOptions')
        if self.zoomScale is not None:
            oprot.writeFieldBegin('zoomScale', TType.DOUBLE, 1)
            oprot.writeDouble(self.zoomScale)
            oprot.writeFieldEnd()
        if self.ifReverse is not None:
            oprot.writeFieldBegin('ifReverse', TType.I32, 2)
            oprot.writeI32(self.ifReverse)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(mapOptions)
mapOptions.thrift_spec = (
    None,  # 0
    (1, TType.DOUBLE, 'zoomScale', None, None, ),  # 1
    (2, TType.I32, 'ifReverse', None, None, ),  # 2
)
fix_spec(all_structs)
del all_structs
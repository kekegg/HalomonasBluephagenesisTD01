import json
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from tdmeta import userService
from tdmeta.ttypes import mapOptions
import json
import hashlib
import pandas as pd
import rdkit.Chem.Draw
from rdkit import Chem
import numpy as np
from meta_model import Tdmeta

if __name__ == "__main__":
    port = 8000
    ip = "127.0.0.1"
    # 创建服务端
    handler = Tdmeta()  # 自定义类
    processor = userService.Processor(handler)  # userService为python接口文件自动生成
    # 监听端口
    transport = TSocket.TServerSocket(ip, port)  # ip与port位置不可交换
    # 选择传输层
    tfactory = TTransport.TBufferedTransportFactory()
    # 选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    # 创建服务端
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # print(handler.getMapData())
    opt = mapOptions()
    opt.zoomScale = 0.5
    handler.getMapData(opt)
    print("start server in python")
    server.serve()
    print("Done")

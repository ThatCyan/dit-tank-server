from socket import *

DIC_DEV = {}


class Server(object):

	def __init__(self,port):
		super(Server, self).__init__()
		self.sock = socket(AF_INET,SOCK_DGRAM)
		self.port = port
	def startServer(self):
		self.sock.bind(('',self.port))
		print("system runing " + str(self.port))
		while True:
			data,addr=self.sock.recvfrom(1024)
			# print(data,addr)
			try:
				self.parserData(data,addr)
			except Exception as e:
				print(e)
				pass
			
			
	def parserData(self,data,addr):
		global DIC_DEV
		dataStr = str(data,encoding='utf-8')
		
		if dataStr.startswith("$"):
			dataStr = dataStr[1:]
			cmds = dataStr.split("@")
			if len(cmds)>1:
				cmd = cmds[0]
				if cmd == "HBT":
					devID = cmds[1]
					
					DIC_DEV[devID] = addr
					print("设备登录")
					print(addr)
				if cmd == "CMD":
					devID = cmds[1]
					
					devAddr = DIC_DEV.get(devID)
					print("转发 "+devID)
					print(devAddr)
					if devAddr!=None:
						self.sock.sendto(data,(devAddr[0],9999))


		else:
			print("failed")
			return
		

def main():
	sever = Server(9999)
	sever.startServer()
if __name__ == '__main__':
	main()
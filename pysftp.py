import paramiko
import sys
import time,datetime
import os
from configparser import ConfigParser

class PySFTP(object):

    def __init__(self):
        cp=ConfigParser()
        path = os.path.abspath('seetings.ini')
        if os.path.exists(path):
            cp.read(path,encoding="utf-8-sig")
        
        self.remotename=cp.get("sftp", "hostname")
        self.remoteport=cp.get("sftp", "port")
        self.loginname=cp.get("sftp", "username")
        self.loginpassword=cp.get("sftp", "password")

        self.transport = self.connectSFTP()

    def connectSFTP(self):

        try:
            remotename=str(self.remotename)
            remoteport=int(self.remoteport)
            tran = paramiko.Transport(remotename,remoteport)
            print('connect success!')
        except Exception as e:
            print('connect failed,reasons are as follows:',e)
        else:
            try:
                tran.connect(username = self.loginname,password = self.loginpassword)
                
                print('login success!')
            except Exception as e:
                print('connect failed,reasons are as follows:',e)
            else:
                return tran

    def download(self,remoteaddress,localaddress,time_ge=None):
        sftp=paramiko.SFTPClient.from_transport(self.transport)
        filelist = sftp.listdir(remoteaddress)
        print('begin downloading!')
        for i in filelist:
            try:           
                if(time_ge is not None):
                    st_mtime=sftp.stat(remoteaddress+'/'+i).st_mtime
                    time_local = time.localtime(st_mtime)
                    dt =datetime.datetime.strptime(time.strftime("%Y-%m-%d",time_local),"%Y-%m-%d") 
                    if(dt<time_ge):
                        continue
                start = time.clock()
                sftp.get(remoteaddress+'/'+i,localaddress+'\\'+i)
                end = time.clock()
                print('success download %s,use time %fs' % (i,(end - start)))               
            except Exception as e:
                print('failed download %s,reason are as follows:' % i,e)
                continue #下载出错继续进行下一步


    
    def upload(self, local_path, remote_dir=''):
        """
        upload file to sftp server
        :param local_path: local file path
        :param remote_dir: remote folder path
        :return:
        """
        if not os.path.isfile(local_path):
            raise FileNotFoundError('File %s is not found' % local_path)

        

        local_name = os.path.basename(local_path)
        remote_path = os.path.join(remote_dir, local_name)
        sftp=paramiko.SFTPClient.from_transport(self.transport)
        sftp.put(local_path, remote_path)



    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result,encoding='utf-8'))
        return result


if __name__ == "__main__":
    sftp=PySFTP()
    client=paramiko.SFTPClient.from_transport(sftp.transport)
    
    print(dt)
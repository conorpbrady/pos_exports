import ftplib
import paramiko

class Connection:

    @staticmethod
    def get_connection_class(connection_type, config):
        if connection_type.lower() == 'FTP'.lower():
            return FTP(config)
        elif connection_type.lower() == 'SFTP'.lower():
            return SFTP(config)
        elif connection_type.lower() == 'cURL'.lower():
            return Curl(config)
        
    def __init__(self, host):
        self.host = host

    def download_file(filename):
        pass

    def upload_file(filename):
        pass


class FTP(Connection):

    def __init__(self, config):

        self.port = int(config['Port'])
        self.user = config['User']
        self.password = config['Password']
        self.use_ssl = (config['UseSSL'] == '1' or
                        config['UseSSL'].lower == 'true')
        super().__init__(config['Host'])

    def connect(self):
        if self.use_ssl:
            self.ftp = ftplib.FTP_TLS(self.host)
            self.ftp.login(self.user,self.password)
            self.ftp.prot_p()
        else:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user,self.password)
        
    def close(self):
        self.ftp.close()

    def change_remote_directory(self, remote_path):
        self.ftp.cwd(remote_path)
        
    def download_file(self, filename):
        with open(filename, 'wb') as w:
            self.ftp.retrbinary('RETR ' + filename, w)

    def upload_file(self, filename):
        self.ftp.storbinary('STOR {}'.format(filename), open(filename,'rb'))
    
                       
class SFTP(FTP):

    def __init__(self, config):
        super().__init(config)

    def connect(self):
        self.transport = paramiko.Transport(self.host,self.port)        
        self.transport.connect(username = self.user,
                               password = self.password)
        self.ftp = paramiko.SFTPClient.from_transport(self.transport)
    
    def close(self):
        self.ftp.close()
        self.transport.close()

    def change_remote_directory(self, remote_path):
        self.ftp.chdir(remote_path)
        
    def download_file(self, filename):
        self.ftp.get(filename, filename)

    def upload_file(self, filename):
        self.ftp.put(filename, filename)

    
class Curl(Connection):

    def __init__(self, config):
        # cmd-line option:
        # >curl -k --header "Csrf-token: nocheck" --form "report=@filename” URL

        self.url = config['Host'] + config['URL_ID']

        c = pycurl.Curl() # curl
        c.setopt(c.SSL_VERIFYPEER, 0) # -k
    
        # --header "csrf-token: nocheck"
        c.setopt(c.HTTPHEADER, ["csrf-token: nocheck"])

        # URL
        c.setopt(c.URL, url)


    def upload_file(self, filename):

        # --form "@report=FILENAME"
        c.setopt(c.POST, 1)
        c.setopt(c.HTTPPOST, [("report", (c.FORM_FILE, filename))])

        # Execute and close
        c.perform()

    def close(self):
        c.close()   




    pass

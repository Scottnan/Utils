import win32service
import win32serviceutil
import win32event
import winerror
import servicemanager
import os, sys, time
# from smco_croniter import SMCOSched


class CronDaemon(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "Cron Daemon"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Cron Daemon"
    # this text shows up as the description in the SCM
    _svc_description_ = "Cron Daemon for scheduled tasks"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def SvcDoRun(self):
        while self.isAlive:
            print("your code")
            time.sleep(10)

    def SvcStop(self):
      self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
      win32event.SetEvent(self.hWaitStop)
      self.isAlive = False


if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(CronDaemon)
            servicemanager.Initialize('CronDaemon', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
        """
        except win32service.error, details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
        """
    else:
        win32serviceutil.HandleCommandLine(CronDaemon)

import os
import subprocess

class WinService:
    """
    The WinService Class is used for controlling services in windows.
    Pass the name of the service you wish to control to the class instance.
	The acceptable name of service is short name, do not pass its display name.
	You can find short name in services.msc and double click on service.
    """

    def __init__(self, servicename):
        self.service = servicename
        self.servicesregkey = "SYSTEM\\CurrentControlSet\\Services\\"
        self.serviceregkey = self.servicesregkey + servicename
        self.statemap = {
			1: "STOPPED",
			2: "STARTING",
			3: "STOPPING",
            4: "RUNNING"
		}
        self.starttypemap = {
			0: "boot",
			1: "system",
			2: "auto",
			3: "demand",
            4: "disabled",
            5: "delayed-auto"
		}

    # Starts service
    def start(self):
        os.system("sc start " + self.service)

	# Stops service (Only if service can be stopped)
    def stop(self):
        os.system("sc stop " + self.service)

	# Restars service
    def restart(self):
        self.stop()
        self.start()

	# Pauses service (Only if service supports feature)
    def pause(self):
        os.system("sc pause " + self.service)

	# Resumes service that has been paused
    def resume(self):
        os.system("sc continue " + self.service)

	# Sets startup type (Boot, System, Automatic, Manual, Disabled)
    def setStartType(self, newtype):
        os.system("sc config " + self.service + " start=" + newtype)

	# Gets service startup type (Boot, System, Automatic, Manual, Disabled)
    def getStartType(self):
        num = self.getStartTypeNum()
        return self.starttypemap.get(int(num))

	# Gets service state type (Stopped, Starting, Stopping, Running)
    def getState(self):
        num = self.getStateNum()
        return self.statemap.get(int(num))

	# Gets service start type num (Boot, System, Automatic, Manual, Disabled)(0-4)
    def getStartTypeNum(self):
        return self.getQCValue("START_TYPE")

	# Gets service state type num (Stopped, Starting, Stopping, Running)(1-4)
    def getStateNum(self):
        return self.getQueryValue("STATE")

	# Gets long name - display name
    def getDisplayName(self):
        return self.getQCValue("DISPLAY_NAME")

	# Gets group service belongs to
    def getGroup(self):
        return self.getQCValue("LOAD_ORDER_GROUP")

	# Can service be stopped?
    def canStop(self):
        output = self.getShellOutput("sc query " + self.service)
        return "NOT_STOPPABLE" not in output

	# Can service be paused?
    def canPause(self):
        output = self.getShellOutput("sc query " + self.service)
        return "NOT_PAUSABLE" not in output

	# Can service be shutdown?
    def canShutdown(self):
        output = self.getShellOutput("sc query " + self.service)
        return "IGNORES_SHUTDOWN" not in output

	# Gets value of argument `argname` from shell command `sc qc servicename`
    def getQCValue(self, argname):
        return self.getValue("sc qc ", argname)

	# Gets value of argument `argname` from shell command `sc qc servicename`
    def getQueryValue(self, argname):
        return self.getValue("sc query ", argname)

	# Gets value of argument `argname` from shell command `command self.service`
    def getValue(self, command, argname):
        output = self.getShellOutput(command + " " + self.service)
        argindex = output.index(argname)
        argnumberindexstart = output.index(":", argindex) + 2
        argnumberindexend = output.index("  ", argnumberindexstart)
        argvalue = ""
        for i in range(argnumberindexstart, argnumberindexend):
            argvalue += output[i]
        return argvalue

	# Gets subprocess.check_output function as string (utf-8)
    def getShellOutput(self, command):
        output = subprocess.check_output(command, shell=True)
        return output.decode("utf-8")

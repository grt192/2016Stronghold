import platform, webbrowser, os, sys
import multiprocessing as mp
from multiprocessing import freeze_support

def main():
	vision_server_url_local = "http://127.0.0.1:5809"


	vision_server_url_remote = "http://roborio-192-frc.local:5809"

	camera1_url = "http://roborio-192-frc.local:5800/stream.html"
	camera2_url = "http://roborio-192-frc.local:5802/stream.html"
	camera3_url = "http://roborio-192-frc.local:5803/stream.html"


	if "Darwin" in platform.platform():
		code_arg_local = "python3.4 ~/git/2016Stronghold/py/robot.py sim"
		dash_arg_local = "java -jar ~/wpilib/tools/SmartDashboard.jar ip 127.0.0.1"
		code_arg_remote = "python3.5 ~/git/2016Stronghold/py/robot.py deploy --skip-tests --no-version-check --nc"
		dash_arg_remote = "java -jar ~/wpilib/tools/SmartDashboard.jar ip roborio-192-frc.local"

	if "Windows" in platform.platform():
		code_arg_local = "py robot.py sim"
		dash_arg_local = "java -jar SmartDashboard.jar ip 127.0.0.1"
		code_arg_remote = "py robot.py deploy --skip-tests --no-version-check --nc"
		dash_arg_remote = "java -jar SmartDashboard.jar ip roborio-192-frc.local"

	if not (len(sys.argv) == 2 or len(sys.argv) == 3):
		print("No arguments provided!")
		exit(0)
	situation = sys.argv[1]
	if situation == "simv":
		os.chdir(os.path.normpath("C:/Users/GRT Student/Desktop/git/2016Stronghold/py"))
		mp.Process(target=os.system, args=(code_arg_local,)).start()
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_local,)).start()
		webbrowser.open(vision_server_url_local, new=1)
	if situation == "sim":
		os.chdir(os.path.normpath("C:/Users/GRT Student/Desktop/git/2016Stronghold/py"))
		mp.Process(target=os.system, args=(code_arg_local,)).start()
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_local,)).start()
	if situation == "dashv":
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_remote,)).start()
		webbrowser.open(camera1_url, new=1)
		webbrowser.open(camera2_url, new=1)
		webbrowser.open(vision_server_url_remote, new=1)
	if situation == "dash":
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_remote,)).start()
		webbrowser.open(camera1_url, new=1)
		webbrowser.open(camera2_url, new=1)
	if situation == "deployv":
		os.chdir(os.path.normpath("C:/Users/GRT Student/Desktop/git/2016Stronghold/py"))
		mp.Process(target=os.system, args=(code_arg_remote,)).start()
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_remote,)).start()
		webbrowser.open(camera1_url, new=1)
		webbrowser.open(camera2_url, new=1)
		webbrowser.open(vision_server_url_remote, new=1)
	if situation == "deploy":
		os.chdir(os.path.normpath("C:/Users/GRT Student/Desktop/git/2016Stronghold/py"))
		mp.Process(target=os.system, args=(code_arg_remote,)).start()
		os.chdir(os.path.normpath("C:/Users/GRT Student/wpilib/tools"))
		mp.Process(target=os.system, args=(dash_arg_remote,)).start()
		webbrowser.open(camera1_url, new=1)
		webbrowser.open(camera2_url, new=1)

if __name__ == "__main__":
	if "Windows" in platform.platform():
		freeze_support()
	main()


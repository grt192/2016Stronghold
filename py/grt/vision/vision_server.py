
from flask import Flask, render_template, Response
import threading
app = Flask(__name__)

class VisionServer:
	def __init__(self, robot_vision):
		self.robot_vision = robot_vision
		self.server_thread = threading.Thread(target=self.start_server)
		self.server_thread.start()


	@app.route('/')
	def index(self):
	    """Video streaming home page."""
	    return render_template('index.html')

	#@staticmethod
	def gen(self):
	    """Video streaming generator function."""
	    while True:
	        frame = self.robot_vision.getFrame()
	        time.sleep(.05)
	        yield (b'--frame\r\n'
	               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	def start_server(self):
	    app.run(host='0.0.0.0', debug=False, threaded=True)

	@app.route('/video_feed')
	def video_feed(self):
	    """Video streaming route. Put this in the src attribute of an img tag."""
	    return Response(self.gen(),
	                    mimetype='multipart/x-mixed-replace; boundary=frame')
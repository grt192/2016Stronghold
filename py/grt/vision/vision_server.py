from flask import Flask, render_template, Response
import threading, time
import numpy as np
import platform
if "Linux" in platform.platform():
    host_ip = 'roborio-192-frc.local'
else:
    host_ip = '0.0.0.0'
app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

#@staticmethod
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.getFrame()[1]
        #print(frame)
        time.sleep(1)
        to_print = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + np.ndarray.tostring(frame) + b'\r\n'
        #print(to_print)
        yield (to_print)


def prepare_module(robot_vision):
    def start_server():
        app.run(host=host_ip, port=5809, debug=False, threaded=True)

    @app.route('/video_feed')
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(robot_vision),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    server_thread = threading.Thread(target=start_server)
    server_thread.start()
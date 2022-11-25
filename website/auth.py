from flask import Blueprint, Flask,render_template,Response, request, flash, redirect, url_for
import cv2
import qrcode
from cryptography.fernet import Fernet
import random
from pyzbar.pyzbar import decode
import numpy as np

auth = Blueprint('auth', __name__)
camera=cv2.VideoCapture(0)


def generate_frames():
    while True:
            
        # reading from the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            # ret,buffer=cv2.imencode('.jpg',frame)
            # frame=buffer.tobytes()

            for code in decode(frame):
                #decoding data 
                decoded_data = code.data.decode('utf-8')

                #checking positioning Rect(left= , top= , width= , height=)
                rect_pts = code.rect

                # sensitivedata = decoded_data + str(random.getrandbits(256))
                # key = Fernet.generate_key()
                # fernet = Fernet(key)
                # global ENCQRCODE
                # ENCQRCODE = fernet.encrypt(sensitivedata.encode())

                if decoded_data:
                    pts = np.array([code.polygon], np.int32)
                    # draw lines around the code
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                    # putting text
                    cv2.putText(frame, str(decoded_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0))

            #cv2.imshow("image", frame)
            #cv2.waitKey(1)
            #camera.release()
            ret, buffer = cv2.imencode('.jpg', frame)
            #convert buffer to bytes
            frame = buffer.tobytes()

            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get("pin")
        if len(pin) == 4:
            return redirect(url_for('auth.account'))
        elif len(pin) < 4:
            flash('Podano za mało cyfr', category='error')
        else:
            flash('Podano za dużo cyfr', category='error')
    return render_template("login.html")

@auth.route('/logout')
def coupons():
    return render_template("coupons.html")

@auth.route('/mycoupons')
def mycouponspytho():
    return render_template("mycoupons.html",data='/static/images/qrcode2746577.png')

@auth.route('/kodylojalnosciowe')
def sign_up():
    return "<p>Sign Up</p>"

@auth.route('/account')
def account():
    return render_template("account.html")

@auth.route('/generate_qr')
def generate_qr():
    sensitivedata = '''{
            "transaction": [
                {
                    "amount": {
                        "currency": "PLN",
                        "total": '5'
                    },
                    "description": "This is the payment transaction description.",
                    "ip": "192.158.1.38",
                    "date": "2015-16-11"
                    "timestamp" ": 12:52:34"
                }
                    "deviceinf": [
                {
                    "os": {android07a9ds"
                    },
                    "device": "POCO Phone 3dad pro",}],}
                    '''
    sensitivedata = str(sensitivedata) + str(random.getrandbits(256))
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(sensitivedata.encode())

    decMessage = fernet.decrypt(encMessage).decode()
    db =[]
    db.append(encMessage)
    keys = []
    for i in db:
            keys.append(random.getrandbits(128))
    input_data = keys[-1]
    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    name = str(random.getrandbits(32))
    img.save('website/static/images/qrcode{}.png'.format(name))
    print('website/static/images/qrcode{}.png'.format(name))
    return render_template("generate.html", image_data='static/images/qrcode{}.png'.format(name))

@auth.route('/scan_qr')
def scan_qr():
    return render_template('scan.html')
    #return "<p>Scan qr code</p>"
    
@auth.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@auth.route('/confirm_payment')
def confirm_payment():
    return render_template('confirm.html')





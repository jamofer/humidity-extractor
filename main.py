#!/usr/bin/env python2

from flask import Flask, request
import humidity_extractor
from humidity_extractor import ExtractorSpeeds
from flask_cors import CORS

PASSWORD = "cW6sZ=7R?z=yGtXV"


app = Flask(__name__)
CORS(app)
configuration = humidity_extractor.load_configuration()
humidity_extractor.start(configuration)


@app.route("/status")
def status():
    current_speed = ExtractorSpeeds.by_ratio(configuration.velocity_ratio)

    return {
        'speeds': [speed.name for speed in ExtractorSpeeds.all()],
        'available_speeds': [speed.name for speed in ExtractorSpeeds.available_speeds()],
        'current': {
            'speed': current_speed.name,
            'ratio': round(configuration.velocity_ratio, ndigits=2),
            'real_ratio': round(ExtractorSpeeds.ratio_for(current_speed), ndigits=2)
        }
    }


@app.route("/doc")
def dock():
    return '''
    GET /configuration -> {"velocity_ratio": float}</br>
    POST /configure -> {"velocity_ratio": 0.0 - 1.0}</br>
    POST /configure -> {"velocity_percentage": 0 - 100}</br>
    POST /configure -> {"velocity": ("off" | "quiet" | "very low" | "normal" | "high" | "very high" | "maximum") }</br>
    '''


@app.route("/configuration", methods=["GET"])
def get_configuration():
    return configuration.__dict__


@app.route("/configure", methods=["POST"])
def configure():
    request_json = request.get_json()

    if request_json is None:
        return '', 400

    if _is_remote_ip_origin():
        if 'pswd' not in request_json or request_json['pswd'] != PASSWORD:
            return '', 403

    if 'velocity_percentage' in request_json:
        request_json['velocity_ratio'] = request_json['velocity_percentage'] / 100.0

    if 'velocity' in request_json:
        speed = ExtractorSpeeds.by_name(request_json['velocity'])
        request_json['velocity_ratio'] = ExtractorSpeeds.ratio_for(speed)

    if 'velocity_ratio' not in request_json:
        return '', 400

    velocity_ratio = request_json['velocity_ratio']
    if velocity_ratio > 1:
        velocity_ratio = 1

    if velocity_ratio < 0:
        velocity_ratio = 0

    configuration.velocity_ratio = velocity_ratio
    humidity_extractor.save_configuration(configuration)
    humidity_extractor.set_velocity(velocity_ratio)

    return "", 200


def _is_remote_ip_origin():
    return not request.remote_addr.startswith('192') and not request.remote_addr.startswith('127')


if __name__ == '__main__':
    app.run('0.0.0.0', port=21000, debug=True)

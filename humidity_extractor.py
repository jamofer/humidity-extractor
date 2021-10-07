import json
import os

from RPi import GPIO


CONFIGURATION_FILE = os.path.expanduser("~/.humidity_extractor.json")


class Speed:
    def __init__(self, name, pin, toggle_pin=False):
        self.name = name
        self.pin = pin
        self.toggle_pin = toggle_pin

    def __repr__(self):
        return 'Velocity({name}, {pin}, toggle_pin={toggle})'.format(name=self.name, pin=self.pin, toggle=self.toggle_pin)


class ExtractorSpeeds(object):
    Velocity1 = Speed('quiet', pin=2)
    Velocity2 = Speed('very_slow', pin=3, toggle_pin=True)
    Velocity3 = Speed('slow', pin=4, toggle_pin=True)
    Velocity4 = Speed('normal', pin=14, toggle_pin=True)
    Velocity5 = Speed('fast', pin=15, toggle_pin=True)
    Velocity6 = Speed('very_fast', pin=17, toggle_pin=True)
    Velocity7 = Speed('maximum', pin=18, toggle_pin=True)
    SpeedOff = Speed("off", pin=None)

    @classmethod
    def all(cls):
        return [
            cls.SpeedOff,
            cls.Velocity1,
            cls.Velocity2,
            cls.Velocity3,
            cls.Velocity4,
            cls.Velocity5,
            cls.Velocity6,
            cls.Velocity7
        ]

    @classmethod
    def available_speeds(cls):
        return [velocity for velocity in cls.all() if velocity.pin is not None or velocity.name == "off"]

    @classmethod
    def by_ratio(cls, ratio):
        number_of_velocities = len(cls.available_speeds())
        velocity_per_ratio = int(round((number_of_velocities - 1) * ratio))

        return cls.available_speeds()[velocity_per_ratio]

    @classmethod
    def ratio_for(cls, speed):
        try:
            return (cls.all().index(speed)) / float(len(cls.all()) - 1)
        except ValueError:
            return 0

    @classmethod
    def by_name(cls, name):
        for speed in cls.all() + [cls.SpeedOff]:
            if name == speed.name:
                return speed

        return None


class Configuration(object):
    def __init__(self, velocity_ratio=0.1):
        self.velocity_ratio = velocity_ratio


def start(configuration):
    GPIO.setmode(GPIO.BCM)

    for velocity in ExtractorSpeeds.available_speeds():
        _initialize_velocity_pin(velocity)

    set_velocity(configuration.velocity_ratio)


def set_velocity(ratio):
    if ratio == 0:
        turn_off()
        return

    velocity_target = ExtractorSpeeds.by_ratio(ratio)
    rest_of_velocities = set(ExtractorSpeeds.available_speeds()) - {velocity_target}

    reset_velocities(rest_of_velocities)

    _set_velocity_pin(velocity_target, enabled=True)


def turn_off():
    reset_velocities(ExtractorSpeeds.available_speeds())


def reset_velocities(rest_of_velocities):
    for velocity in rest_of_velocities:
        _set_velocity_pin(velocity, enabled=False)


def _initialize_velocity_pin(velocity):
    if velocity is ExtractorSpeeds.SpeedOff:
        return

    GPIO.setup(velocity.pin, GPIO.OUT, initial=_velocity_pin_value(velocity, enabled=False))


def _set_velocity_pin(velocity, enabled):
    if velocity is ExtractorSpeeds.SpeedOff:
        return

    gpio_value = _velocity_pin_value(velocity, enabled)
    GPIO.output(velocity.pin, gpio_value)


def _velocity_pin_value(velocity, enabled):
    if velocity.toggle_pin:
        enabled = not enabled

    return GPIO.HIGH if enabled else GPIO.LOW


def load_configuration():
    if not os.path.exists(CONFIGURATION_FILE):
        return Configuration()

    with open(CONFIGURATION_FILE) as f:
        json_configuration = json.loads(f.read())
        return Configuration(json_configuration["velocity_ratio"])


def save_configuration(configuration):
    with open(CONFIGURATION_FILE, 'w') as f:
        json_configuration = json.dumps(configuration.__dict__)
        return f.write(json_configuration)

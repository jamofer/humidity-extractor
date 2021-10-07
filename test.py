import unittest
from mock import patch, call

import fake_rpigpio.utils
fake_rpigpio.utils.install()

from RPi import GPIO
import humidity_extractor
from humidity_extractor import ExtractorSpeeds, Configuration


class TestHumidityExtractor(unittest.TestCase):
    def teardown(self):
        patch.stopall()

    def test_velocity_per_ratio(self):
        assert ExtractorSpeeds.by_ratio(0) == ExtractorSpeeds.SpeedOff
        assert ExtractorSpeeds.by_ratio(0.07) == ExtractorSpeeds.SpeedOff
        assert ExtractorSpeeds.by_ratio(0.1) == ExtractorSpeeds.Velocity1
        assert ExtractorSpeeds.by_ratio(0.15) == ExtractorSpeeds.Velocity1
        assert ExtractorSpeeds.by_ratio(0.30) == ExtractorSpeeds.Velocity2
        assert ExtractorSpeeds.by_ratio(0.45) == ExtractorSpeeds.Velocity3
        assert ExtractorSpeeds.by_ratio(0.60) == ExtractorSpeeds.Velocity4
        assert ExtractorSpeeds.by_ratio(0.75) == ExtractorSpeeds.Velocity5
        assert ExtractorSpeeds.by_ratio(0.90) == ExtractorSpeeds.Velocity6
        assert ExtractorSpeeds.by_ratio(0.95) == ExtractorSpeeds.Velocity7

    def test_start(self):
        setmode = patch('RPi.GPIO.setmode').start()
        setup = patch('RPi.GPIO.setup').start()
        output = patch('RPi.GPIO.output').start()
        conf = Configuration(velocity_ratio=0.1)

        humidity_extractor.start(conf)

        setmode.assert_called_once_with(GPIO.BCM)
        setup.assert_has_calls([
            call(2, GPIO.OUT, initial=GPIO.LOW),
            call(3, GPIO.OUT, initial=GPIO.HIGH),
        ])
        output.assert_has_calls([
            call(3, GPIO.HIGH),
            call(2, GPIO.HIGH),
        ])

    def test_ratio_for(self):
        assert ExtractorSpeeds.ratio_for(ExtractorSpeeds.Velocity1) == 1/7.0

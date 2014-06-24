from __future__ import unicode_literals

import unittest

import alsaaudio

import mock

from mopidy_alsamixer.mixer import AlsaMixer


@mock.patch('mopidy_alsamixer.mixer.alsaaudio', spec=alsaaudio)
class MixerTest(unittest.TestCase):

    def setUp(self):
        self.config = {'alsamixer': {'card': 0, 'control': 'Master'}}
        self.mixer = AlsaMixer(self.config)

    def test_has_config(self, alsa_mock):
        self.assertEqual(self.mixer.config, self.config)

    def test_use_card_from_config(self, alsa_mock):
        alsa_mock.cards.return_value = ['PCH', 'SB']
        alsa_mock.mixers.return_value = ['Master']
        self.config = {'alsamixer': {'card': 1, 'control': 'Master'}}
        self.mixer = AlsaMixer(self.config)

        self.mixer.get_volume()

        alsa_mock.Mixer.assert_called_once_with(control='Master', cardindex=1)

    def test_fails_if_card_is_unknown(self, alsa_mock):
        alsa_mock.cards.return_value = ['PCH', 'SB']
        alsa_mock.mixers.return_value = ['Master']
        self.config = {'alsamixer': {'card': 2, 'control': 'Master'}}

        with self.assertRaises(SystemExit):
            self.mixer = AlsaMixer(self.config)

    def test_use_control_from_config(self, alsa_mock):
        alsa_mock.cards.return_value = ['PCH', 'SB']
        alsa_mock.mixers.return_value = ['Speaker']
        self.config = {'alsamixer': {'card': 0, 'control': 'Speaker'}}
        self.mixer = AlsaMixer(self.config)

        self.mixer.get_volume()

        alsa_mock.Mixer.assert_called_once_with(control='Speaker', cardindex=0)

    def test_fails_if_control_is_unknown(self, alsa_mock):
        alsa_mock.cards.return_value = ['PCH', 'SB']
        self.config = {'alsamixer': {'card': 0, 'control': 'Speaker'}}

        with self.assertRaises(SystemExit):
            self.mixer = AlsaMixer(self.config)

    def test_get_volume(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getvolume.return_value = [86]

        self.assertEqual(self.mixer.get_volume(), 86)

        mixer_mock.getvolume.assert_called_once_with()

    def test_get_volume_when_channels_are_different(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getvolume.return_value = [86, 70]

        self.assertIsNone(self.mixer.get_volume())

        mixer_mock.getvolume.assert_called_once_with()

    def test_get_volume_when_no_channels(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getvolume.return_value = []

        self.assertIsNone(self.mixer.get_volume())

        mixer_mock.getvolume.assert_called_once_with()

    def test_set_volume(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value

        self.assertTrue(self.mixer.set_volume(74))

        mixer_mock.setvolume.assert_called_once_with(74)

    def test_get_mute_when_muted(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getmute.return_value = [1]

        self.assertIs(self.mixer.get_mute(), True)

        mixer_mock.getmute.assert_called_once_with()

    def test_get_mute_when_unmuted(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getmute.return_value = [0]

        self.assertIs(self.mixer.get_mute(), False)

        mixer_mock.getmute.assert_called_once_with()

    def test_set_mute_to_muted(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value

        self.assertTrue(self.mixer.set_mute(True))

        mixer_mock.setmute.assert_called_once_with(1)

    def test_get_mute_when_channels_are_different(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value
        mixer_mock.getmute.return_value = [0, 1]

        self.assertIs(self.mixer.get_mute(), None)

        mixer_mock.getmute.assert_called_once_with()

    def test_set_mute_to_unmuted(self, alsa_mock):
        mixer_mock = alsa_mock.Mixer.return_value

        self.assertTrue(self.mixer.set_mute(False))

        mixer_mock.setmute.assert_called_once_with(0)

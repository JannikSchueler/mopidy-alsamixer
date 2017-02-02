from __future__ import unicode_literals

import os

from mopidy import config, ext


__version__ = '1.0.3'


class Extension(ext.Extension):

    dist_name = 'Mopidy-ALSAMixer'
    ext_name = 'alsamixer'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['card'] = config.Integer(minimum=0)
        schema['control'] = config.String()
        schema['volmin'] = config.Integer(minimum=0, maximum=100)
        schema['volmax'] = config.Integer(minimum=0, maximum=100)
        schema['logarithmic_volume'] = config.Boolean()
        return schema

    def setup(self, registry):
        from mopidy_alsamixer.mixer import AlsaMixer

        registry.add('mixer', AlsaMixer)

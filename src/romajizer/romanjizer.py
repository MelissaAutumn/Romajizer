PLUGIN_NAME = "Retrieve English Alias"
PLUGIN_AUTHOR = "Melissa Autumn (OopsAllNaps)"
PLUGIN_DESCRIPTION = """Selects the primary English alias of an artist."""
PLUGIN_VERSION = '1.0'
PLUGIN_API_VERSIONS = ['2.2']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

from picard.metadata import register_track_metadata_processor
from picard.plugin import PluginPriority

def transliterate_track(album, metadata, track, release):
    artists_list = track.get('artist-credit', [])

    artists = []
    for artist in artists_list:
        found = False
        aliases = artist.get('artist', {}).get('aliases', [])
        for alias in aliases:
            if alias.get('primary', True) and alias.get('locale') == 'en':
                artists.append(alias.get('name'))
                found = True
                break

    if len(artists) > 0:
        metadata['artist'] = ', '.join(artists)


register_track_metadata_processor(transliterate_track, priority=PluginPriority.HIGH)

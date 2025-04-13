PLUGIN_NAME = "Primary Alias Retriever"
PLUGIN_AUTHOR = "Melissa Autumn (OopsAllNaps)"
PLUGIN_DESCRIPTION = """Selects the primary English alias of an artist."""
PLUGIN_VERSION = '1.0'
PLUGIN_API_VERSIONS = ['2.2']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

from picard.metadata import register_track_metadata_processor
from picard.plugin import PluginPriority

#print("[Primary Alias Retriever] Registered")

def get_primary_alias(album, metadata, track, release):
    #print("[Primary Alias Retriever] get_primary_alias")
    artists_list = track.get('artist-credit', [])

    artists = []
    for artist in artists_list:
        aliases = artist.get('artist', {}).get('aliases', [])
        for alias in aliases:
            if alias.get('primary', True) and alias.get('locale') == 'en':
                artists.append(alias.get('name'))
                break

    if len(artists) > 0:
        metadata['artist'] = ', '.join(artists)


register_track_metadata_processor(get_primary_alias, priority=PluginPriority.HIGH)

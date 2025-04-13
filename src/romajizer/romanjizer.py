PLUGIN_NAME = "Romajizer"
PLUGIN_AUTHOR = "Melissa Autumn (OopsAllNaps)"
PLUGIN_DESCRIPTION = """Selects the primary English alias of an artist.

Falls back to transliterating Japanese text to the Latin/Roman alphabet using pykakasi.

If pykakasi is not found in the system install of Python then it transliterating features will be disabled.

If transliterating please double check spelling against known sources (vgmdb is a good one.)
"""
PLUGIN_VERSION = '1.0'
PLUGIN_API_VERSIONS = ['2.2']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

try:
    import pykakasi

    kks = pykakasi.kakasi()
except ImportError:
    print("[Romajizer] pykakasi was not found. Disabling transliterating features.\n")
    pykakasi = None
    kks = None

from picard.metadata import register_track_metadata_processor
from picard.plugin import PluginPriority


def transliterate(text: str, is_name: bool = False):
    if kks is None:
        return text

    results = kks.convert(text)

    str_builder = []
    for result in results:
        # If the value is the same then we don't need to do anything here...
        if result['hepburn'] == text:
            return text

        # Going off vibes here...
        if is_name:
            romaji = result['passport'].capitalize()
        else:
            romaji = result['hepburn']
        str_builder.append(romaji)

    if is_name:
        str_builder = list(reversed(str_builder))

    return ' '.join(str_builder)


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

        if found:
            continue

        # Fallback to transliterating
        name = artist.get('artist', {}).get('name')
        if name:
            artists.append(name)

    trans_artists = []
    for artist in artists:
        trans_artists.append(transliterate(artist, True))

    if len(trans_artists) > 0:
        metadata['artist'] = ', '.join(trans_artists)


register_track_metadata_processor(transliterate_track, priority=PluginPriority.HIGH)

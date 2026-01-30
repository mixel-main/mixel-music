import asyncio
import hashlib
import json
import mimetypes
import re
import unicodedata
from typing import Any

from tinytag import TinyTag, Image, Images

from app.infra.path import get_path, str_path


DATE_PATTERNS = {
    "year_month_day": re.compile(r"^(\d{4})[-., ]?(\d{1,2})[-., ]?(\d{1,2})$"),
    "year_month": re.compile(r"^(\d{4})[-., ]?(\d{1,2})$"),
    "year": re.compile(r"^(\d{4})$"),
}
FEAT_RE = re.compile(r"\b(feat\.?|ft\.?|featuring|with)\b", re.IGNORECASE)
SPLIT = re.compile(r"\s*(?:;|\s+/\s+)\s*") # ';' or ' / ' only
_WS = re.compile(r"\s+")


def _nfkc(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("\u00A0", " ")
    return _WS.sub(" ", s).strip()


def _hash(s: str) -> str:
    return hashlib.md5(s.encode("utf-8"), usedforsecurity=False).hexdigest()


def get_mime(path: str) -> str:
    try:
        mime, _enc = mimetypes.guess_type(path, strict=True)
        return mime or 'application/octet-stream'
    except Exception:
        return 'application/octet-stream'


def normalize_text(v: Any) -> str:
    if v is None:
        return ''
    try:
        return _nfkc(str(v))
    except Exception:
        return ''


def normalize_date(date: int | str | None) -> tuple[str, int]:
    date = normalize_text(date)
    if not date:
        return '', 0

    m = DATE_PATTERNS["year_month_day"].match(date)
    if m:
        year, month, day = m.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}", int(year)
    
    m = DATE_PATTERNS["year_month"].match(date)
    if m:
        year, month = m.groups()
        return f"{year}-{month.zfill(2)}", int(year)
    
    m = DATE_PATTERNS["year"].match(date)
    if m:
        year = m.group(1)
        return year, int(year)
    
    return '', 0


def _get_other_casefold(other: Any, key: str) -> Any:
    if other is None:
        return None
    
    if isinstance(other, dict):
        lk = key.casefold()
        for k, v in other.items():
            if str(k).casefold() == lk:
                return v
            
    return None


def _get_other_multiple(other: Any, keys: list[str]) -> list[str]:
    for key in keys:
        v = _get_other_casefold(other, key)
        if v is None:
            continue

        try:
            sv = safe_list(other, key)
            if sv not in (None, "", []):
                v = sv
        except Exception:
            pass

        if isinstance(v, (list, tuple, set)):
            return [normalize_text(x) for x in v if normalize_text(x)]
        
        if isinstance(v, str):
            v = normalize_text(v)
            if "\x00" in v:
                parts = [normalize_text(x) for x in v.split("\x00")]
                return [p for p in parts if p]
            
            return [v] if v else []
        
        s = normalize_text(v)
        return [s] if s else []

    return []


def make_id(
    type: str,
    data: str,
    version: str = 'v1'
) -> str:
    data = f"{version}|{type}|{data}"
    hash = _hash(data)

    import uuid
    return str(uuid.UUID(hex=hash))


def make_album_id(tags: TinyTag) -> str:
    other = getattr(tags, 'other', None)

    mbz_albumid = _get_other_casefold(other, 'musicbrainz_albumid')
    if mbz_albumid:
        mbz_albumid = normalize_text(mbz_albumid)
        if mbz_albumid:
            return make_id('album', f"mbid:{mbz_albumid}")

    data = '|'.join(
        [
            f"album={normalize_text(getattr(tags, 'album', None))}",
            f"albumartist={normalize_text(getattr(tags, 'albumartist', None))}",
        ]
    )

    return make_id('album', data)


def split_feat(artist: str) -> tuple[list[str], list[str]]:
    s = normalize_text(artist)
    if not s:
        return [], []

    m = FEAT_RE.search(s)
    if not m:
        main_raw = s
        feat_raw = ""
    else:
        main_raw = s[:m.start()]
        feat_raw = s[m.end():]

    main = [p for p in (normalize_text(x) for x in SPLIT.split(main_raw)) if p]
    feat = [p for p in (normalize_text(x) for x in SPLIT.split(feat_raw)) if p]

    return main, feat


def split_participants(artist: str) -> list[dict[str, Any]]:
    main, feat = split_feat(artist)
    parts: list[dict[str, Any]] = []

    for name in main:
        canonical = normalize_text(name)
        parts.append(
            {
                "artist_id": make_id('artist', canonical),
                "artist": name,
                "role": "main",
            }
        )

    for name in feat:
        canonical = normalize_text(name)
        parts.append(
            {
                "artist_id": make_id('artist', canonical),
                "artist": name,
                "role": "feat",
            }
        )

    return parts


def safe_list(extra, key, default='') -> str:
    extra = dict(extra)
    
    try:
        value = extra.get(key, [default])
        return value[0] if value else default
    except:
        return ''


def _extract_tags(path: str) -> dict[str, Any]:
    filepath = str_path(path)
    real_path = get_path(path)
    content_type = get_mime(filepath)

    base: dict[str, Any] = {
        "album": "",
        "album_id": '00000000-0000-0000-0000-000000000000',
        "albumartist": "",
        "albumartist_id": '00000000-0000-0000-0000-000000000000',
        "albumartistsort": "",
        "artist": "",
        "artist_id": '00000000-0000-0000-0000-000000000000',
        "artistsort": "",
        "barcode": "",
        "bitdepth": 0,
        "channels": 0,
        "comment": "",
        "compilation": False,
        "composer": "",
        "content_type": content_type,
        "copyright": "",
        "date": "",
        "discnumber": 0,
        "duration": 0.0,
        "filepath": filepath,
        "filesize": 0.0,
        "genre": "",
        "isrc": "",
        "label": "",
        "lyrics": "",
        "musicbrainz_albumartistid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_albumid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_artistid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_discid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_originalalbumid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_originalartistid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_recordingid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_releasegroupid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_trackid": "00000000-0000-0000-0000-000000000000",
        "musicbrainz_workid": "00000000-0000-0000-0000-000000000000",
        "participants": "[]",
        "releasecountry": "",
        "samplerate": 0,
        "subtitle": "",
        "title": "",
        "titlesort": "",
        "totaldiscs": 0,
        "totaltracks": 0,
        "track_id": '00000000-0000-0000-0000-000000000000',
        "tracknumber": 0,
        "year": 0,
    }

    try:
        tags = TinyTag.get(real_path)
    except Exception:
        return base

    other = getattr(tags, "other", None)
    date_str, year_int = normalize_date(getattr(tags, "year", None))
    
    artist = normalize_text(getattr(tags, 'artist', None))
    albumartist = normalize_text(getattr(tags, 'albumartist', None))

    artists = _get_other_multiple(other, ['artists', 'ARTISTS'])
    albumartists = _get_other_multiple(other, ['albumartists', 'ALBUMARTISTS'])

    participants: list[dict[str, Any]] = []

    if artists:
        for name in artists:
            canonical = normalize_text(name)
            participants.append(
                {
                    "artist_id": make_id('artist', canonical),
                    "artist": name,
                    "role": "main",
                }
            )
    else:
        participants = split_participants(artist)

    first_id = None
    for p in participants:
        if p.get('role') == 'main':
            first_id = p.get('artist_id')
            break

    if albumartists:
        first_artist = albumartists[0]
        albumartist_id = make_id('artist', normalize_text(first_artist))
    else:
        if albumartist:
            albumartist_id = make_id('artist', normalize_text(albumartist))
        else:
            albumartist_id = None


    album_id = make_album_id(tags)
    track_id = _hash(path)

    base.update(
        {
            "album": tags.album or '',
            "album_id": album_id,
            "albumartist": albumartist,
            "albumartist_id": albumartist_id,
            "albumartistsort": safe_list(tags.other, 'albumartistsort'),
            "albumsort": safe_list(tags.other, 'albumsort'),
            "artist": artist,
            "artist_id": first_id,
            "artistsort": safe_list(tags.other, 'artistsort'),
            "barcode": safe_list(tags.other, 'barcode'),
            "bitdepth": tags.bitdepth or 0,
            "bitrate": tags.bitrate or 0.0,
            "channels": tags.channels or 0,
            "comment": tags.comment or '',
            "compilation": True if safe_list(tags.other, 'compilation') else False,
            "composer": tags.composer or '',
            "copyright": safe_list(tags.other, 'copyright'),
            "date": date_str,
            "discnumber": tags.disc or 0,
            "duration": tags.duration or 0.0,
            "filesize": tags.filesize or 0.0,
            "genre": tags.genre or '',
            "isrc": safe_list(tags.other, 'isrc'),
            "label": safe_list(tags.other, 'label'),
            "lyrics": safe_list(tags.other, 'lyrics'),
            "musicbrainz_albumartistid": safe_list(tags.other, 'musicbrainz_albumartistid'),
            "musicbrainz_albumid": safe_list(tags.other, 'musicbrainz_albumid'),
            "musicbrainz_artistid": safe_list(tags.other, 'musicbrainz_artistid'),
            "musicbrainz_discid": safe_list(tags.other, 'musicbrainz_discid'),
            "musicbrainz_originalalbumid": safe_list(tags.other, 'musicbrainz_originalalbumid'),
            "musicbrainz_originalartistid": safe_list(tags.other, 'musicbrainz_originalartistid'),
            "musicbrainz_recordingid": safe_list(tags.other, 'musicbrainz_recordingid'),
            "musicbrainz_releasegroupid": safe_list(tags.other, 'musicbrainz_releasegroupid'),
            "musicbrainz_trackid": safe_list(tags.other, 'musicbrainz_trackid'),
            "musicbrainz_workid": safe_list(tags.other, 'musicbrainz_workid'),
            "participants": json.dumps(participants, ensure_ascii=False),
            "releasecountry": safe_list(tags.other, 'releasecountry'),
            "samplerate": tags.samplerate or 0,
            "title": tags.title or '',
            "titlesort": safe_list(tags.other, 'titlesort'),
            "totaldiscs": tags.disc_total or 0,
            "totaltracks": tags.track_total or 0,
            "track_id": track_id,
            "tracknumber": int(getattr(tags, "track", None) or 0),
            "year": year_int,
        }
    )

    return base


def _extract_imgs(path: str) -> bytes | None:
    try:
        tag: TinyTag = TinyTag.get(get_path(path), image=True)

        images: Images = tag.images
        if not images:
            return None

        front: Image | None = getattr(images, "front_cover", None)
        if front and getattr(front, "data", None):
            return front.data

        back: Image | None = getattr(images, "back_cover", None)
        if back and getattr(back, "data", None):
            return back.data

        try:
            first = next(iter(images))
            return first.data if first and getattr(first, "data", None) else None
        except Exception:
            return None
        
    except Exception:
        return None


async def extract_tags(path: str) -> dict[str, Any]:
    return await asyncio.to_thread(_extract_tags, path)


async def extract_imgs(path: str) -> bytes | None:
    return await asyncio.to_thread(_extract_imgs, path)

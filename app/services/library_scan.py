import asyncio
from app.models import Album, Artist, Track
from app.core.database import db_conn, func, exists, select
from app.core.logger import get_logger
from app.repos.library import LibraryRepo

logger = get_logger()

class LibraryScan:
    @staticmethod
    async def perform_all() -> None:
        await asyncio.gather(
            LibraryScan.perform_albums(),
            LibraryScan.perform_artists(),
            return_exceptions=True,
        )

    @staticmethod
    async def perform_albums() -> None:
        logger.debug("Performing Albums...")

        async with db_conn() as conn:
            db_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.albumartist_id,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                )
                .where(
                    Track.album_id != '',
                )
                .group_by(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.track_total,
                )
            )

            db_result = await conn.execute(db_query)
            albums_data = db_result.all()

            for alb in albums_data:
                album_data = {
                    'album': alb.album,
                    'album_id': alb.album_id,
                    'albumartist_id': alb.albumartist_id,
                    'disc_total': alb.disc_total,
                    'year': alb.year,
                }

                await LibraryRepo(conn).insert_album(album_data)

            unknown_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.artist,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                )
                .where(Track.album == '')
                .group_by(
                    Track.artist,
                    Track.directory,
                )
            )

            unknown_result = await conn.execute(unknown_query)
            unknown_albums_data = unknown_result.all()

            for alb in unknown_albums_data:
                album_data = {
                    'album': alb.album,
                    'album_id': alb.album_id,
                    'albumartist_id': '',
                    'disc_total': alb.disc_total,
                    'year': alb.year,
                }

                await LibraryRepo(conn).insert_album(album_data)

        async with db_conn() as conn:
            albums_query = select(Album.album_id)
            result = await conn.execute(albums_query)
            album_hash = {row.album_id for row in result}

            tracks_query = select(Track.album_id).distinct()
            result = await conn.execute(tracks_query)
            track_hash = {row.album_id for row in result}

            orphan_albums = album_hash - track_hash

            for album_id in orphan_albums:
                logger.debug("Removing Album... (%s)", album_id)
                await LibraryRepo(conn).delete_album(album_id)

    @staticmethod
    async def perform_artists() -> None:
        logger.debug("Performing Artists...")

        async with db_conn() as conn:
            db_query = (
                select(
                    Track.albumartist_id,
                    Track.albumartist,
                )
                .where(Track.albumartist != '')
                .group_by(Track.albumartist_id, Track.albumartist)
            )

            db_result = await conn.execute(db_query)
            artists_data = db_result.all()

            for art in artists_data:
                artist_data = {
                    'artist': art.albumartist,
                    'artist_id': art.albumartist_id,
                }
                
                await LibraryRepo(conn).insert_artist(artist_data)

        async with db_conn() as conn:
            orphan_albumartists_query = (
                select(Artist.artist_id)
                .where(
                    ~exists(
                        select(1)
                        .where(Track.albumartist_id == Artist.artist_id)
                    )
                )
            )

            result = await conn.execute(orphan_albumartists_query)
            orphan_albumartists = {row[0] for row in result}

            for artist_id in orphan_albumartists:
                logger.debug("Removing Artist... (%s)", artist_id)
                await LibraryRepo(conn).delete_artist(artist_id)

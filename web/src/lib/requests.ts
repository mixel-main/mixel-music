import type {
  AlbumListResponse,
  AlbumResponse,
  TrackListResponse,
  TrackResponse,
  ArtistListResponse,
  ArtistResponse
} from "./interface";
import { apiFetch } from "./tools";


export async function postLogout(
  fetch: typeof window.fetch
): Promise<void> {
  
  try {
    const postLogout = await fetch(
      `http://localhost:8000/api/auth/logout`,
      {
        method: 'POST',
        credentials: 'include',
      }
    );

    if (!postLogout.ok) {
      throw new Error(postLogout.statusText);
    }

    window.location.href = '/signin';

  }

  catch (error) {
    console.error('Logout failed:', error);
    throw new Error('Failed to log out');
  }
}


export async function getTracks(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: TrackListResponse;}> {

  try {
    const fetchTracks = await apiFetch(fetch,
      `http://localhost:8000/api/tracks?offset=${start}&limit=${end}`);

    if (!fetchTracks.ok) {
      throw new Error(fetchTracks.statusText);
    }

    const response: TrackListResponse = await fetchTracks.json();

    return {
      response,
    };
  }
  
  catch (error) {
    return {
      response: {
        "items": [],
        "total": 0,
      },
    }
  }
};


export async function getTrack(
  fetch: typeof window.fetch,
  trackId: string,
): Promise<{response: TrackResponse;}> {
  
  try {
    const fetchTrack = await apiFetch(fetch,
      `http://localhost:8000/api/tracks/${trackId}`);

    if (!fetchTrack.ok) {
      throw new Error(fetchTrack.statusText);
    }

    const response: TrackResponse = await fetchTrack.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getAlbums(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: AlbumListResponse;}> {

  try {
    const fetchAlbums = await apiFetch(fetch,
      `http://localhost:8000/api/albums?offset=${start}&limit=${end}`);

    if (!fetchAlbums.ok) {
      throw new Error(fetchAlbums.statusText);
    }

    const response: AlbumListResponse = await fetchAlbums.json();

    return {
      response,
    };
  }

  catch (error) {
    return {
      response: {
        "items": [],
        "total": 0,
      },
    }
  }
};


export async function getAlbum(
  fetch: typeof window.fetch,
  albumId: string,
): Promise<{response: AlbumResponse;}> {

  try {
    const fetchAlbum = await apiFetch(fetch,
      `http://localhost:8000/api/albums/${albumId}`);

    if (!fetchAlbum.ok) {
      throw new Error(fetchAlbum.statusText);
    }

    const response: AlbumResponse = await fetchAlbum.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getArtists(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{response: ArtistListResponse;}> {

  try {
    const fetchArtists = await apiFetch(fetch,
      `http://localhost:8000/api/artists?offset=${start}&limit=${end}`);

    if (!fetchArtists.ok) {
      throw new Error(fetchArtists.statusText);
    }

    const response: ArtistListResponse = await fetchArtists.json();

    return {
      response,
    };
  }

  catch (error) {
    return {
      response: {
        "items": [],
        "total": 0,
      },
    }
  }
};


export async function getArtist(
  fetch: typeof window.fetch,
  artistId: string,
): Promise<{response: ArtistResponse;}> {

  try {
    const fetchArtist = await apiFetch(fetch,
      `http://localhost:8000/api/artists/${artistId}`);

    if (!fetchArtist.ok) {
      throw new Error(fetchArtist.statusText);
    }

    const response: ArtistResponse = await fetchArtist.json();

    return {
      response,
    };
  }

  catch (error) {
    throw error;
  }
};

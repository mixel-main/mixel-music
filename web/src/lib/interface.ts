export interface ListResponse<T> {
  items: T[];
  total: number;
}

export interface TrackSummary {
  album: string;
  album_id: string;
  artist: string;
  artist_id: string;
  duration: number;
  title: string;
  track_id: string;
}

export type TrackListResponse = ListResponse<TrackSummary>;

export interface TrackDetail {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  artist: string;
  artist_id: string;
  barcode?: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  compilation: boolean;
  comment?: string;
  composer?: string;
  content_type: string;
  copyright?: string;
  created_at?: string;
  date?: string;
  director?: string;
  directory: string;
  duration: number;
  disc_number: number;
  disc_total: number;
  filepath: string;
  filesize: number;
  genre?: string;
  isrc?: string;
  label?: string;
  lyrics?: string;
  samplerate: number;
  title: string;
  track_id: string;
  track_number: number;
  track_total: number;

  updated_at: string;
  year?: number;
}

export type TrackResponse = TrackDetail;

export interface AlbumTrack {
  artist: string;
  artist_id: string;
  comment?: string;
  duration: number;
  title: string;
  track_id: string;
  track_number: number;
}

export interface AlbumSummary {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  year?: number;
}

export type AlbumListResponse = ListResponse<AlbumSummary>;

export interface AlbumDetail {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  disc_total: number;
  year?: number;
  tracks: AlbumTrack[];
}

export type AlbumResponse = AlbumDetail;

export interface ArtistAlbum {
  album: string;
  album_id: string;
  albumartist_id: string;
  year?: number;
}

export interface ArtistSummary {
  artist: string;
  artist_id: string;
  album_total: number;
  track_total: number;
}

export type ArtistListResponse = ListResponse<ArtistSummary>;

export interface ArtistDetail extends ArtistSummary {
  duration_total: number;
  filesize_total: number;
  albums: ArtistAlbum[];
}

export type ArtistResponse = ArtistDetail;

export interface PlayerState {
  index: number;
  lists: TrackSummary[];
  isLoaded: boolean;
  isPlaying: boolean;
  currentTime: number;
  volumeRange: number;
  duration: number;
  volume: number;
  mute: boolean;
  loop: number;
}

export interface PlayerStore extends PlayerState, TrackSummary {
  artwork?: string;
}

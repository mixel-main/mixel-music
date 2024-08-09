export interface TrackListResponse {
  list: TrackList[];
  total: number;
}

export interface TrackList {
  title: string;
  album: string;
  artist: string;
  hash: string;
  albumhash: string;
}

export interface TrackItem {
  hash: string;
  title: string;
  artist: string;
  artisthash: string;
  album: string;
  albumhash: string
  albumartist: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  comment: string;
  composer: string;
  disc: number;
  disctotal: number;
  duration: number;
  size: number;
  genre: string;
  samplerate: number;
  track: number;
  tracktotal: number;
  year: string;
  directory: string;
  mime: string;
  path: string;
  created_date: Date;
  updated_date: Date;
  lyrics: string;
  isrc: string;
}

export interface AlbumListResponse {
  list: AlbumList[];
  total: number;
}

export interface AlbumList {
  albumhash: string;
  album: string;
  albumartist: string;
  albumartisthash: string;
  year: string;
  durationtotals: number;
  tracktotals: number;
  disctotals: number;
  sizetotals: number;
}

export interface AlbumItem {
  albumhash: string;
  album: string;
  albumartist: string;
  albumartisthash: string;
  year: string;
  durationtotals: number;
  tracktotals: number;
  disctotals: number;
  sizetotals: number;
  tracks: TrackItem[];
}

export interface ArtistListResponse {
  list: ArtistList[];
  total: number;
}

export interface ArtistList {
  artisthash: string;
  artist: string;
}

export interface ArtistItem {
  artisthash: string;
  artist: string;
}
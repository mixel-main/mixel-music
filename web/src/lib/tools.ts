export function getArtwork(hash: string, size: number): string {
  let artwork: string =
    `http://localhost:2843/api/artwork/${hash}?size=${size.toString()}`;

  return artwork;
}

export function getNextPage(page: number = 1, item: number = 40, total: number = 0) {
  const nextPage = total - (page * item) < 1 ? page : page + 1;
  return `?page=${nextPage}&item=${item}`
}

export function getPrevPage(page: number = 1, item: number = 40) {
  const prevPage = page - 1 < 1 ? 1 : page - 1;
  return `?page=${prevPage}&item=${item}`
}

export function convertDateTime(time: number): string {
  const min = Math.floor(time / 60);
  const sec = Math.floor(time % 60);

  return `${ min }:${ sec < 10 ? '0' : '' }${ sec }`;
}

export function convertFileSize(size: number): string {
  const units = ['B', 'KB', 'MB', 'GB'];
  let index = 0;

  while (size >= 1024 && index < units.length - 1) {
    size /= 1024;
    index++;
  }

  return `${size.toFixed(2)} ${units[index]}`;
}
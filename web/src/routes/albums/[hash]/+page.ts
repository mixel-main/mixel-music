import { getAlbumItem } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const hash: string = params.hash

  try {
    const data = await getAlbumItem(fetch, hash);

    return {
      item: data.item!,
      title: data.item.album,
    };
  }
  catch (error) {
    console.error(error);
  }
};
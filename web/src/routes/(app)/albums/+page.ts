import { getAlbums } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const offset = parseInt(url.searchParams.get('offset') ?? '1', 10);
  const limit = parseInt(url.searchParams.get('limit') ?? '40', 10);

  try {
    const data = await getAlbums(fetch, offset, limit);

    return {
      items: data.response,
      title: 'albums.title',
      offset: offset,
      limit: limit,
    };
  }
  catch (error) {
    console.error(error);
  }
};

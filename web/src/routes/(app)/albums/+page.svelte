<script lang="ts">
  import type { PageData } from './$types';
  import type { AlbumListResponse } from '$lib/interface';
  import { getPaginatedList, getAlbumLink, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import GridItemDetail from '$lib/components/elements/GridItemDetail.svelte';
  import { _ } from 'svelte-i18n';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let albums: AlbumListResponse = $state(data.items);
  let startNumber = data.offset;
  let loading = false;

  async function loadMoreAlbums() {
    if (loading || (startNumber + 39) >= albums.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'album', albums.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      albums = {
        items: [...albums.items, ...response.response.items],
        total: response.response.total,
      };
    }

    loading = false;
  }
</script>


<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

<InfiniteScroll threshold={100} on:loadMore={loadMoreAlbums}>
{#snippet renderAlbum({ item })}
  <GridItem
    href={getAlbumLink(item.album_id)}
    src={item.album_id}
    alt={item.album ?? $_('unknown_album')}
  >
    <GridItemDetail
      title={item.album ?? $_('unknown_album')}
      titleHref={getAlbumLink(item.album_id)}
      sub={item.albumartist}
      subHref={getArtistLink(item.albumartist_id)}
    />
  </GridItem>
{/snippet}

<GridWrap
  items={albums.items}
  renderItem={renderAlbum}
/>
</InfiniteScroll>

<script lang="ts">
  import type { PageData } from './$types';
  import { getAlbumLink } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import GridItemDetail from '$lib/components/elements/GridItemDetail.svelte';
  import { _ } from 'svelte-i18n'

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

<svelte:head>
  <title>{data.item.artist} • mixel-music</title>
</svelte:head>

<PageTitle title={data.item.artist} />

{#if data.item}
  <GridWrap items={data.item.albums}>
    {#snippet GridItem({ item })}
        <GridItem
        
        
        href={getAlbumLink(item.album_id)}
        src={item.album_id}
        alt={item.album}
        lazyload
      >
        <GridItemDetail
          title={item.album ? item.album : $_('unknown_album')}
          titleHref={getAlbumLink(item.album_id)}
          sub={item.year != 0 ? $_('info.year',{values: {year: item.year}}) : $_('unknown_year')}
        />
      </GridItem>
      {/snippet}
  </GridWrap>
{/if}

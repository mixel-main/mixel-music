<script lang="ts">
  import type { PageData } from './$types';
  import type { TrackListResponse } from '$lib/interface';
  import {
    removeLinkParams,
    getPaginatedList,
  } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';
  import TrackTable from '$lib/components/TrackTable.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let tracks: TrackListResponse = $state(data.items);
  let startNumber: number = data.offset;
  let endNumber: number = data.limit

  async function changePage(direction: 'next' | 'prev') {
    const { newStart, newEnd, response } = await getPaginatedList(
      fetch,
      direction,
      'track',
      data.tracks.total,
      startNumber,
      39,
    );

    startNumber = newStart;
    endNumber = newEnd;

    if (response) {
      tracks = {
        items: [...response.response.items],
        total: response.response.total
      };
    }

    removeLinkParams(
      { start: startNumber.toString(), end: (endNumber).toString() }
    );
  }
</script>


<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

{#if data.tracks}
  <div style="margin-bottom: var(--space-s);">
    <ControlsBar tracks={tracks.items} />
  </div>

  <TrackTable tracks={tracks.items} />

  <div class='bottom-ctl'>
    <Button
      button='round'
      preload='hover'
      iconName='iconoir:nav-arrow-left'
      on:click={() => changePage('prev')}
    />
    
    <Button
      button='round'
      preload='hover'
      iconName='iconoir:nav-arrow-right'
      disabled={data.end + (data.end - data.start) >= data.tracks.total}
      on:click={() => changePage('next')}
    />
  </div>
{/if}


<style>
  .bottom-ctl {
    gap: 12px;
    display: flex;
    justify-content: flex-end;
    margin: var(--space-m) 0;
  }
</style>

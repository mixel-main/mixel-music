<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  import type { AlbumResponse } from "$lib/interface";
  import { 
    getArtistLink,
    convertDateTime
  } from "$lib/tools";
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import PlayerService from "$lib/stores/stores";
  import TrackDropdown from "./TrackDropdown.svelte";
  import { _ } from 'svelte-i18n';

  interface Props {
    list: AlbumResponse;
  }

  let { list }: Props = $props();
</script>


<Table>
  <TableHead>
    <TableHeadItem size='xs'>#</TableHeadItem>
    <TableHeadItem size='xl'>{$_('label.title')}</TableHeadItem>
    <TableHeadItem size='l'>{$_('label.artist')}</TableHeadItem>
    <TableHeadItem size="s">{$_('label.time')}</TableHeadItem>
    <TableHeadItem size="xs"></TableHeadItem>
  </TableHead>

  {#each list.tracks as item}
    <TableBody>
      <TableBodyItem size='xs'>
          <span class="text-sub normal">
            {item.track_number != 0 ? item.track_number : '-'}
          </span>
        </TableBodyItem>
      <TableBodyItem size='xl'>
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <!-- svelte-ignore a11y_missing_attribute -->
        <a onclick={() =>
          PlayerService.addTrack(
            [{
              album: list.album,
              album_id: list.album_id,
              artist: item.artist,
              artist_id: item.artist_id,
              duration: item.duration,
              title: item.title,
              track_id: item.track_id,
            }]
          , true)}
        onkeydown={bubble('keydown')}>
          {item.title}
        </a>
      </TableBodyItem>

      <TableBodyItem size='l'>
        <a href='{getArtistLink(item.artist_id)}'>
          {item.artist}
        </a>
      </TableBodyItem>

      <TableBodyItem size='s'>
        {convertDateTime(item.duration)}
      </TableBodyItem>
      
      <TableBodyItem size='xs'>
        <TrackDropdown track={{
            album: list.album,
            album_id: list.album_id,
            artist: item.artist,
            artist_id: item.artist_id,
            duration: item.duration,
            title: item.title,
            track_id: item.track_id
          }}
        />
      </TableBodyItem>

    </TableBody>
  {/each}

</Table>

<script lang="ts">
  import {
    getAlbumLink,
    getArtistLink,
    getArtwork,
    convertDateTime,
  } from "$lib/tools";
  import PlayerService from "$lib/stores/stores";
  import ArtworkImage from "$lib/components/elements/ArtworkImage.svelte";
  import { _ } from 'svelte-i18n'

  let trk = $derived($PlayerService);
</script>

<div class="player-info">
  {#if trk.track_id}
    <ArtworkImage
      src={trk.album === ''
        ? getArtwork(trk.track_id, 128)
        : trk.album_id && getArtwork(trk.album_id, 128)
      }
      alt={$_('player.front_cover')}
      width=60
      height=60
    />

    <div>
      <span class="text bold">{trk.title}</span>
      <span class="text-sub">
        <a href="{getArtistLink(trk.artist_id)}">
          {trk.artist}
        </a> -
        <a href="{getAlbumLink(trk.album_id)}">
          {trk.album ? trk.album : $_('unknown_album')}
        </a>  
      </span>
      <span class="text-sub">
        {convertDateTime(trk.currentTime)} / {convertDateTime(trk.duration)}
      </span>
    </div>
  {/if}
</div>

<style>
  .player-info {
    display: flex;
    align-items: center;
    gap: var(--space-s);
  }

  .player-info div {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    height: 100%;
  }
</style>

<script lang="ts">
  export let album: string;
  export let albumartist: string;
  export let year: string;
  export let totalTracks: number;
  export let totalLength: number | string;
  export let comment: string = '';
  export let size: string | number;
</script>

<div class="album-header">
  <div class="album-main">
    <span class="album-title">
      {album}
    </span>

    <span class="album-artist">
      {albumartist}
    </span>
  </div>

  <div class="album-info">
    <span class="album-text">
      {#if totalTracks === 1}
        {totalTracks} Track
      {:else}
        {totalTracks} Tracks
      {/if}
      ({totalLength}) · {year} · {size}
    </span>
    <span class="album-text">
      {comment}
    </span>
  </div>
</div>

<style>
  .album-header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: -webkit-fill-available;
    gap: 24px;
  }

  .album-main {
    display: flex;
    flex-direction: column;
  }

  .album-title {
    font-size: clamp(1rem, 2vw, 2rem);
    font-weight: 800;
    text-overflow: ellipsis;
    /* text-wrap: nowrap; */
    overflow: hidden;
  }

  .album-info {
    display: flex;
    flex-direction: column;
  }

  .album-artist {
    font-size: 110%;
    color: var(--color-dark-text-2);
  }

  .album-text {
    font-size: 80%;
    line-height: 1rem;
    color: var(--color-dark-text-2);
  }
</style>
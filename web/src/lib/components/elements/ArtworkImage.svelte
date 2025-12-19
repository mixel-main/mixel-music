<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  interface Props {
    alt?: string | undefined;
    src?: string | undefined;
    width?: string | number | undefined;
    height?: string | number | undefined;
    FullCover?: boolean;
    lazyload?: boolean;
  }

  let {
    alt = undefined,
    src = undefined,
    width = undefined,
    height = undefined,
    FullCover = false,
    lazyload = true
  }: Props = $props();
  
  let showArtwork = $state(true);
  
</script>


<div style="height: {height}px;">
  {#if showArtwork}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <img
      loading={lazyload ? "lazy" : "eager"}
      {src}
      {alt}
      {width}
      {height}
      onclick={bubble('click')}
      onkeydown={bubble('keydown')}
      onmousedown={bubble('mousedown')}
      onmouseleave={bubble('mouseleave')}
      onerror={() => showArtwork = !showArtwork}
      class:full={FullCover}
    />
  {/if}
</div>


<style>
  div {
    aspect-ratio: 1/1;
    display: flex;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-s);
  }

  img {
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
    object-fit: scale-down;
    user-select: none;
    -webkit-user-drag: none;
  }

  .full {
    object-fit: cover;
  }
</style>

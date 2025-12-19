<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  import { getArtwork } from "$lib/tools";
  import ArtworkImage from "./ArtworkImage.svelte";

  interface Props {
    href?: string | undefined;
    alt?: string | undefined;
    src?: string | undefined;
    children?: import('svelte').Snippet;
  }

  let {
    href = undefined,
    alt = undefined,
    src = undefined,
    children
  }: Props = $props();
</script>


<div class="grid-item">
  {#if src}
    <a
      data-sveltekit-preload-data tabindex="-1" onclick={bubble('click')} {href}>
      <ArtworkImage src={getArtwork(src, 300)} {alt}/>
    </a>
    {@render children?.()}

  {:else}
    <!-- svelte-ignore a11y_missing_content -->
    <a data-sveltekit-preload-data tabindex="-1" onclick={bubble('click')} {href}></a>
    {@render children?.()}

  {/if}
</div>


<style>
  .grid-item {
    white-space: nowrap;
    margin-bottom: var(--space-m);
  }

  a {
    user-select: none;
    -webkit-user-drag: none;
  }
</style>

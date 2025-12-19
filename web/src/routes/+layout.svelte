<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import { page } from '$app/state';
  import { afterNavigate } from '$app/navigation';
  import PlayerService from '$lib/stores/stores';
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();

  let previousPathname: string | null = null;

  afterNavigate(() => {
    const currentPathname = page.url.pathname;
    
    if (previousPathname == null || currentPathname !== previousPathname) {
      document.getElementById("contents")?.scrollIntoView({
        block: "start",
        inline: "nearest",
      });
    }

    previousPathname = currentPathname;
  });

  onDestroy(() => {
    PlayerService.destroy();
  })
</script>


<div id="app">
  {@render children?.()}
</div>


<style>
  #app {
    width: 100%;
    display: flex;
    height: 100dvh;
  }
</style>

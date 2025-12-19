<script lang="ts">
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  
  interface Props {
    threshold?: number;
    children?: import('svelte').Snippet;
  }

  let { threshold = 2000, children }: Props = $props();
  const dispatch = createEventDispatcher();
  let contentContainer: HTMLElement;

  function onScroll() {
    const { scrollTop, scrollHeight, clientHeight } = contentContainer;
    if (scrollHeight - scrollTop - clientHeight <= threshold) {
      dispatch('loadMore');
    }
  }

  onMount(() => {
    contentContainer = document.querySelector('#wrap');
    if (contentContainer) {
      contentContainer.addEventListener('scroll', onScroll);
    }

    return () => {
      if (contentContainer) {
        contentContainer.removeEventListener('scroll', onScroll);
      }
    };
  });
</script>

{@render children?.()}

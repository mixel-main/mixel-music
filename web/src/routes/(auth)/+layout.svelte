<script lang="ts">
  import '../style.css';
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>


<div id="wrap">
  {@render children?.()}
</div>


<style>
  #wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--space-m);
    flex-direction: column;
  }
</style>
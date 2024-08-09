<script lang="ts">
  import PageHead from "./page-head.svelte";
  export let title: string | undefined = undefined;
</script>

<PageHead {title} />

<div>
  <slot />
</div>

<style>
  div {
    display: grid;
    grid-gap: 21px;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    overflow-x: hidden;
  }
</style>
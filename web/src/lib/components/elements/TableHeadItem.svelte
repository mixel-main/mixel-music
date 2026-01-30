<script lang="ts">
  interface Props {
    size?: string;
    children?: import('svelte').Snippet;
  }

  let { size = 'm', children }: Props = $props();

  let flexSize = $derived({
    xs: 0.1,
    s: 1,
    m: 2,
    l: 3,
    xl: 5
  }[size] || 1);
</script>


<div style={`flex: ${flexSize};`}>
  {@render children?.()}
</div>


<style>
  div {
    font-size: 75%;
    font-weight: bold;
    color: var(--dark-text-sub);
    text-transform: uppercase;
    letter-spacing: 0.3px;
    padding: var(--table-pad);
  }
</style>

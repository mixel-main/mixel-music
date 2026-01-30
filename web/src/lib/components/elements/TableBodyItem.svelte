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

  let additionalStyle = $derived(size === 'xs' ? 'text-overflow: clip; max-height: 50px;' : '');
</script>


<div style={`flex: ${flexSize}; ${additionalStyle}`}>
  {@render children?.()}
</div>


<style>
  div {
    padding: var(--table-pad);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>

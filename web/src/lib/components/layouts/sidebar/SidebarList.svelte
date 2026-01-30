<script lang="ts">
  interface Props {
    name?: string | undefined;
    children?: import('svelte').Snippet;
  }

  let { name = undefined, children }: Props = $props();
</script>

<ul title={name}>
  {@render children?.()}
</ul>

<style>
  ul[title]::before {
    display: flex;
    font-size: 85%;
    color: var(--dark-text-sub);
    content: attr(title);
    margin-top: var(--space-l);
    margin-left: var(--space-m);
    margin-bottom: var(--space-xs);
  }

  ul {
    list-style: none;
  }
</style>

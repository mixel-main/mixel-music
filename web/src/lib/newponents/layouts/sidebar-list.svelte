<script lang="ts">
  export let name: string | undefined = undefined;
</script>

<ul title={name}>
  <slot />
</ul>

<style>
  ul[title]::before {
    display: flex;
    font-size: 85%;
    margin-top: 36px;
    margin-bottom: 12px;
    content: attr(title);
    color: var(--color-dark-text-2);
  }

  ul {
    list-style: none;
  }
</style>
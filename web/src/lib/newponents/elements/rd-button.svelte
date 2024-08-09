<script lang="ts">
  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let width: string | number | undefined = 42;
  export let height: string | number | undefined = 42;
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  style='width: {width}px; height: {height}px;'
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  class="rd-button"
  on:click
  on:focus
  {href}
>
  <slot />
</svelte:element>

<style>
  .rd-button {
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-text-2);
    background-color: var(--color-dark-bg-2);
    border: 1px solid var(--color-dark-border);
    transition: 0.2s ease;
    border-radius: 50%;
    font-size: 18px;
  }

  .rd-button:hover {
    color: var(--color-dark-text-1);
    transition: 0.2s ease;
  }
</style>
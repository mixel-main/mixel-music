<script lang="ts">
  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let width: string = '42px';
  export let height: string = '42px';
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  style:height={height}
  style:width={width}
  class="sq-button"
  on:click
  on:focus
  {href}
>
  <slot />
</svelte:element>

<style>
  .sq-button {
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-text-2);
    background-color: var(--color-dark-bg-2);
    border: 1px solid var(--color-dark-border);
    transition: 0.2s ease;
    font-size: 18px;
  }

  .sq-button:hover {
    color: var(--color-dark-text-1);
    transition: 0.2s ease;
  }
</style>
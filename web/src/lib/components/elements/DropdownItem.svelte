<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  import Icon from '@iconify/svelte';
  interface Props {
    icon?: string | undefined;
    href?: string | undefined;
    children?: import('svelte').Snippet;
  }

  let { icon = undefined, href = undefined, children }: Props = $props();
</script>

<li>
  <a {href} onclick={bubble('click')}>
    {#if icon}
      <span>
        <Icon {icon} />
      </span>
    {/if}

    {@render children?.()}
  </a>
</li>

<style>
  li {
    list-style: none;
    padding: 0 12px;
    border-radius: var(--radius-m);
  }

  a {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    width: 100%;
    font-size: 15px;
    padding: 6px 12px;
    padding-right: 18px;
    border-radius: var(--radius-m);
    text-decoration: none;
  }

  a:hover,
  a:focus,
  a:active {
    outline-offset: 8px;
  }

  a:hover {
    background-color: var(--black-4);
  }

  span {
    min-height: 36px;
    display: flex;
    font-size: 21px;
    color: var(--dark-text-sub);
    align-items: center;
    justify-content: center;
  }
</style>

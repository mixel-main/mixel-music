<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  import Icon from "@iconify/svelte";

  interface Props {
    type?: string | undefined;
    href?: string | undefined;
    title?: string | undefined;
    button?: string;
    state?: string;
    iconName?: string;
    iconSize?: string;
    width?: string;
    height?: string;
    preload?: string;
    children?: import('svelte').Snippet;
    [key: string]: any
  }

  let {
    type = undefined,
    href = undefined,
    title = undefined,
    button = '',
    state = 'normal',
    iconName = '',
    iconSize = '',
    width = '',
    height = '',
    preload = 'false',
    children,
    ...rest
  }: Props = $props();
</script>


<!-- svelte-ignore a11y_no_static_element_interactions -->
<svelte:element
  class:round={button == 'round'}
  class:square={button == 'square'}
  class:custom={button == 'custom'}
  class:acrylic={state == 'acrylic'}
  data-sveltekit-preload-data={preload}
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  title={title}
  style:width={width}
  style:height={button != 'round' ? height : width}
  {...rest}
  onclick={bubble('click')}
  onfocus={bubble('focus')}
  {href}
>
  {#if iconName}
    <Icon
      icon={iconName}
      width={iconSize}
    />
  {/if}

  {@render children?.()}
</svelte:element>


<style>
  .round {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    transition: 0.2s ease;
    font-weight: 500;
    font-size: 18px;

    border-radius: var(--radius-l);
    padding: calc(var(--space-xs) + 3px);
    text-decoration: none;
  }

  .square {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    transition: 0.2s ease;
    font-weight: 500;
    font-size: 15px;

    border-radius: var(--radius-s);
    padding: var(--space-xs);
    gap: var(--space-xs);
    text-decoration: none;
  }

  .custom {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    padding: 0;
    font-size: 16px;
    width: 100%;
    background-color: transparent;
    transition: 0.2s ease;
    text-decoration: none;
    border: none;
  }

  .custom:focus {
    outline: none;
  }

  .acrylic {
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    background-color: var(--dark-queue);
    backdrop-filter: blur(64px);
  }

  a:hover, button:hover {
    color: var(--dark-text);
    transition: 0.2s ease;
  }
</style>

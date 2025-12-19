<script lang="ts">
  import { createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  import Icon from '@iconify/svelte';
  
  interface Props {
    alt?: string;
    off?: boolean;
    icon?: string;
    text?: string;
    disabled?: boolean;
    ControlButton?: boolean;
    PrimaryButton?: boolean;
  }

  let {
    alt = '',
    off = false,
    icon = '',
    text = '',
    disabled = false,
    ControlButton = false,
    PrimaryButton = false
  }: Props = $props();
</script>

<button
  onclick={bubble('click')}
  title={alt}
  class:off={off}
  class:control={ControlButton}
  class:primary={PrimaryButton}
  aria-disabled={disabled}
  {disabled}
>
  {#if icon}
    <Icon
      {icon}
      width={PrimaryButton ? '29' : '23'}
      height={PrimaryButton ? '29' : '23'}
    />
  {/if}

  {text}
</button>

<style>
  button {
    display: flex;
    padding: 12px;
    border: none;
    transition: 0.2s ease;
    color: var(--dark-text);
    background-color: transparent;
    justify-content: center;
    align-items: center;
  }

  button:focus {
    outline: none;
  }

  button:hover {
    color: var(--dark-hover);
    transition: all 0.2s ease;
  }

  button:active {
    color: var(--dark-active);
  }

  .control {
    width: 32px;
    height: 32px;
    padding: 3px;
  }

  .off {
    color: var(--dark-disabled);
  }
</style>

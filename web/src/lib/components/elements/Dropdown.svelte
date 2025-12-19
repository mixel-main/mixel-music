<script lang="ts">
  import Button from "./Button.svelte";
  import { onMount, onDestroy, tick } from "svelte";
  import { fade } from "svelte/transition";

  let isDropdownOpen = $state(false);
  interface Props {
    dropdownStyle?: string;
    dropdownWidth?: string;
    dropdownOpenIcon?: string | undefined;
    dropdownCloseIcon?: string | undefined;
    children?: import('svelte').Snippet;
  }

  let {
    dropdownStyle = 'round',
    dropdownWidth = '',
    dropdownOpenIcon = undefined,
    dropdownCloseIcon = $bindable(undefined),
    children
  }: Props = $props();

  let dropdownElement: HTMLElement | null = $state(null);
  let buttonElement: HTMLElement | null = $state(null);
  let dropdownPosition = $state({ top: 0, left: 0 });
  let wrapElement: HTMLElement | null = null;

  if (dropdownCloseIcon === undefined && dropdownOpenIcon) {
    dropdownCloseIcon = dropdownOpenIcon;
  }

  const calculateDropdownPosition = async () => {
    await tick();

    if (!buttonElement || !dropdownElement) return;
    const buttonRect = buttonElement.getBoundingClientRect();
    const dropdownRect = dropdownElement.getBoundingClientRect();

    const parentStyle = window.getComputedStyle(buttonElement.offsetParent as Element);
    const isSticky =
      parentStyle.position === "sticky" &&
      buttonElement.offsetParent?.getBoundingClientRect().top === 0;

    const scrollX = isSticky ? 0 : wrapElement?.scrollLeft || window.scrollX;
    const scrollY = isSticky ? 0 : wrapElement?.scrollTop || window.scrollY;

    let top = buttonRect.bottom + scrollY + 12;
    let left = buttonRect.left + scrollX;

    if (top + dropdownRect.height > scrollY + window.innerHeight - 96 - 10) { // 96: Player Height
      top = buttonRect.top + scrollY - dropdownRect.height - 12;
    }

    if (left + dropdownRect.width > scrollX + window.innerWidth) {
      left = buttonElement.offsetLeft - dropdownElement.offsetWidth + buttonRect.width;
    }

    dropdownPosition = {
      top: Math.max(0, top),
      left: Math.max(0, left),
    };
  };

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;

    if (isDropdownOpen) {
      calculateDropdownPosition(); // 드롭다운 열릴 때 위치 계산

      if (wrapElement) {
        wrapElement.style.overflow = 'hidden';
      }
    }
    else {
      if (wrapElement) {
        wrapElement.style.overflow = '';
      }
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownElement && !dropdownElement.contains(event.target as Node) &&
      buttonElement && !buttonElement.contains(event.target as Node)
    ) {
      if (wrapElement) {
        wrapElement.style.overflow = '';
      }
      isDropdownOpen = false;
    }
  };

  onMount(() => {
    wrapElement = document.getElementById("wrap");
    document.addEventListener("click", handleClickOutside);
  });

  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
</script>

<div bind:this={buttonElement} class="dropdown">
  <Button
    button={dropdownStyle}
    iconName={isDropdownOpen ? dropdownCloseIcon : dropdownOpenIcon}
    on:click={handleDropdownClick}
    aria-expanded={isDropdownOpen}
    aria-controls="dropdown-menu"
  />
</div>

{#if isDropdownOpen}
  <div
    bind:this={dropdownElement}
    id="dropdown-menu"
    class="dropdown-content"
    style="
      position: absolute;
      top: {dropdownPosition.top}px;
      left: {dropdownPosition.left}px;
      width: {dropdownWidth || 'max-content'};
    "
    in:fade={{ duration: 100 }}
    out:fade={{ duration: 100 }}
  >
    {@render children?.()}
  </div>
{/if}

<style>
  .dropdown {
    display: inline-block;
  }

  .dropdown-content {
    background-color: var(--black-3);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    border-radius: var(--radius-m);
    z-index: 1000;
    overflow: hidden;
    padding: 12px 0;
  }
</style>

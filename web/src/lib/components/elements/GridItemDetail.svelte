<script lang="ts">
  interface Props {
    center?: boolean;
    title: string;
    titleHref?: any;
    sub?: string | undefined;
    subHref?: any;
  }

  let {
    center = false,
    title,
    titleHref = undefined,
    sub = undefined,
    subHref = undefined
  }: Props = $props();
</script>


<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class:center={center}>
  <a href={titleHref} class="text bold">{title}</a>
  {#if sub}
    {#if subHref}
      <a href={subHref} class="text-sub">
        {sub}
      </a>
    {:else}
      <span class="text-sub">{sub}</span>
    {/if}
  {/if}
</div>


<style>
  div {
    padding-top: var(--space-s);
  }

  a {
    width: auto;
    display: block;
    text-overflow: ellipsis;
    overflow: hidden;
    line-height: 150%;
  }

  .center {
    text-align: center;
  }
</style>
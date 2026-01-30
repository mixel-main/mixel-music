<script lang="ts">
  import { convertDateTime, convertFileSize } from "$lib/tools";
  import { _ } from "svelte-i18n";

  interface Props {
    comment?: string;
    year?: number;
    trackTotal?: number;
    durationTotal?: number;
    fileSizeTotal?: number;
  }

  let {
    comment = '',
    year = 0,
    trackTotal = 0,
    durationTotal = 0,
    fileSizeTotal = 0
  }: Props = $props();
</script>


<div class="detail">
  {#if trackTotal === 1}
    {$_('info.track',{values: {track_total: trackTotal}})},
    {convertDateTime(durationTotal)}
    <br>
  {:else}
    {$_('info.tracks',{values: {track_total: trackTotal}})},
    {convertDateTime(durationTotal)}
    <br>
  {/if}

  {year != 0 ? $_('info.year',{values: {year: year}}) : $_('unknown_year')},
  {convertFileSize(fileSizeTotal)}
  <br>

  {#if comment}
    {comment}
  {/if}
</div>


<style>
  .detail {
    font-size: 85%;
    font-weight: 500;
    color: var(--dark-text-sub);
    text-transform: uppercase;
    padding-top: var(--space-l);
  }
</style>

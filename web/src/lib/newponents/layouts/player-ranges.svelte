<script lang="ts">
  export let width: string;
  export let value: number = 0;
  export let name: string = 'range';
</script>

<div
  on:click
  on:keydown
  on:mousedown
  tabindex="0"
  role="slider"
  aria-valuenow={value}
  aria-valuemin="0"
  aria-valuemax="100"
  class={`range-ctl ${name}`}
  style={`width: ${width};`}
>
  <div
    style:width='{value}%'
    class="range-ctl__now"
  />
</div>

<style>
  .range-ctl {
    background-color: var(--color-dark-trk-len);
    border-radius: calc(var(--app-radius) * 2);
    background-clip: content-box;
    cursor: pointer;
    padding: 8px;
  }

  .range-ctl__now {
    width: 0;
    height: 3px;
    justify-content: left;
    background-color: var(--color-dark-trk-now);
    border-radius: var(--app-radius);
  }
</style>
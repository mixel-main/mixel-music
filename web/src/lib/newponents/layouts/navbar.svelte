<script lang="ts">
  import RdButton from '$lib/newponents/elements/rd-button.svelte';
  import TextBox from '$lib/newponents/elements/textbox.svelte';
  import Icon from '@iconify/svelte';
</script>

<nav>
  <div>
    <RdButton on:click={() => history.back()}>
      <Icon icon="iconoir:nav-arrow-left" />
    </RdButton>
    <RdButton on:click={() => history.forward()}>
      <Icon icon="iconoir:nav-arrow-right" />
    </RdButton>
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder="Search"
    />
    <RdButton>
      <Icon icon="iconoir:refresh" />
    </RdButton>
    <RdButton>
      <Icon icon="iconoir:user" />
    </RdButton>
  </div>
</nav>

<style>
  nav {
    position: sticky;
    max-width: 100%;
    top: 0;

    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 0;
  }

  div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
</style>
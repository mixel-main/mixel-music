<script lang="ts">
  import './style.css';
  import Sidebar from '$lib/newponents/layouts/sidebar.svelte';
  import Navbar from '$lib/newponents/layouts/navbar.svelte';
  import Player from '$lib/newponents/layouts/player.svelte';
</script>

<div id="app">
  <Sidebar />

  <section>
    <Navbar />
    <slot />
  </section>

  <Player />
</div>

<style>
  #app {
    width: 100%;
    display: flex;
    height: 100dvh;
    flex-direction: row;
    box-sizing: border-box;
  }

  section {
    width: 100%;
    padding: 64px;
    padding-top: 0;
    margin-bottom: 96px;
    overflow-y: scroll;
    user-select: none;
  }

  section:focus {
    outline: none;
  }
</style>
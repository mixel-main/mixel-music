<script lang="ts">
  import SidebarList from './sidebar-list.svelte';
  import SidebarLink from './sidebar-link.svelte';
</script>

<div>
  <SidebarList>
    <SidebarLink href='/'>
      Home
    </SidebarLink>
    <SidebarLink href='/'>
      Search
    </SidebarLink>
    <SidebarLink href='/'>
      My Mix
    </SidebarLink>
  </SidebarList>

  <SidebarList name='Library'>
    <SidebarLink href='/albums' icon='iconoir:compact-disc'>
      Albums
    </SidebarLink>
    <SidebarLink href='/artists' icon='iconoir:microphone'>
      Artists
    </SidebarLink>
    <SidebarLink href='/tracks' icon='iconoir:music-double-note'>
      Tracks
    </SidebarLink>
  </SidebarList>

  <SidebarList name='Playlists'>
    <SidebarLink href='' icon='iconoir:plus'>
      Create Playlist
    </SidebarLink>
  </SidebarList>
</div>

<style>
  div {
    z-index: 0;
    width: 240px;
    flex-shrink: 0;
    min-height: 100dvh;
    padding: 24px 21px;
    background-color: var(--color-dark-bg-2);
    border-right: 1px solid var(--color-dark-border);
  }
</style>
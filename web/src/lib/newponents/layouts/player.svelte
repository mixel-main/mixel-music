<script lang="ts">
  import { onDestroy } from 'svelte';

  import { getArtwork, convertDateTime } from '$lib/tools';
  import { hash, title, album, artist, albumhash } from '$lib/stores/track';

  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import PlayerButton from './player-button.svelte';
  import PlayerRanges from './player-ranges.svelte';
  import AlbumCover from '$lib/components/albums/album-cover.svelte';

  let musicItem: HTMLAudioElement = new Audio();
  let coverPath: string = getArtwork('', 128);
  let current: number = 0;
  let length: number = 0;

  let lengthBar: number = 0;
  let volumeBar: number = 100;
  let isPlay: boolean = false;
  let isDrag: boolean = false;
  let isLoop: number = 0;

  $: $hash, streamMusic(), setMusicInfo();
  $: musicItem.volume, volumeBar = musicItem.volume * 100;

  function streamMusic(): void {
    if ($hash !== undefined) {
      musicItem.src = `http://localhost:2843/api/stream/${$hash}`;
      coverPath = getArtwork($hash, 128);

      musicItem.addEventListener("loadedmetadata", handleMetadataLoaded);
      musicItem.addEventListener("timeupdate", handleTimeUpdate);
    }
  }

  function handleMetadataLoaded() {
    length = musicItem.duration;
    musicItem.play();
    isPlay = true;
  }

  function handleTimeUpdate() {
    current = musicItem.currentTime;
    if (!isDrag) lengthBar = (current / length) * 100;

    if (current >= musicItem.duration) {
      musicItem.pause();
      isPlay = false;
    }
  }

  function toggleMusic(): void {
    if ($hash) {
      if (musicItem.paused) {
        musicItem.play();
        isPlay = true;
      } else {
        musicItem.pause();
        isPlay = false;
      }
    }
  }

  function playPrev(): void {
    musicItem.currentTime = 0;
  }

  function playNext(): void {
    console.debug("playNext()");
  }

  function setMusicInfo(): void {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: $title,
        album: $album,
        artist: $artist,
        artwork: [{src: $album === 'Unknown Album'
            ? getArtwork($hash, 128) : getArtwork($albumhash, 128)
          }],
      });

      navigator.mediaSession.setActionHandler('play', toggleMusic);
      navigator.mediaSession.setActionHandler('pause', toggleMusic);
      navigator.mediaSession.setActionHandler('seekbackward', () => { musicItem.currentTime -= 10; });
      navigator.mediaSession.setActionHandler('seekforward', () => { musicItem.currentTime += 10; });
      navigator.mediaSession.setActionHandler('previoustrack', playPrev);
      navigator.mediaSession.setActionHandler('nexttrack', playNext);
    }
  }

  function handleSeek(event: MouseEvent, type: string, callback: (value: number) => void): void {
    event.preventDefault();
    const ctl = document.querySelector(type);
    
    if (ctl) {
      const ctlWidth = ctl.clientWidth;
      const ctlBound = ctl.getBoundingClientRect();
      const newValue = Math.max(0, Math.min(event.clientX - ctlBound.left, ctlWidth));

      callback(newValue / ctlWidth);
    }
  }

  function handleDrag(event: MouseEvent, type: 'length' | 'volume'): void {
    isDrag = true;
    event.preventDefault();

    const moveHandler = type === 'length' ? seekLength : seekVolume;
    const postHandler = () => {
      document.removeEventListener("mousemove", moveHandler);
      document.removeEventListener("mouseup", postHandler);

      if (type === 'length' && musicItem) {
        musicItem.currentTime = current - 0.1;
        // 0.1을 붙여야 오른쪽 끝 드래그 > 재생 > 오른쪽 끝 드래그 시 이벤트 안 먹히는 문제 방지
        // 왜 그런 건지는 잘 모르겠음. 여유가 없어서 그런가? 쨌든 나중에 고쳐야 함
      }

      isDrag = false;
    };

    document.addEventListener("mousemove", moveHandler);
    document.addEventListener("mouseup", postHandler);
    moveHandler(event);
  }

  function seekLength(event: MouseEvent): void {
    handleSeek(event, '.length', (value) => {
      if (musicItem && $hash) {
        current = value * length;
        lengthBar = value * 100;

        if (!isDrag) {
          musicItem.currentTime = current;
        }
      }
    });
  }

  function seekVolume(event: MouseEvent): void {
    handleSeek(event, '.volume', (value) => {
      if (musicItem) {
        musicItem.muted = false;
        musicItem.volume = value;
      }
    });
  }

  function muteMusic(): void {
    if (musicItem.volume === 0) {
      musicItem.volume = 1;
      musicItem.muted = false;
    } else {
      musicItem.muted = !musicItem.muted;
    }
  }

  function loopMusic(): void {
    if (isLoop === 0) {
      isLoop = 1;
      musicItem.loop = true;
    } else if (isLoop === 1) {
      isLoop = 2;
      musicItem.loop = true;
    } else {
      isLoop = 0;
      musicItem.loop = false;
    }
  }

  onDestroy(() => {
    if (musicItem) {
      musicItem.src = '';
    }
  });
</script>

<div class="player">
  <div class="player-center">
    <div class="player-button">
      {#key isPlay}
        <PlayerButton
          on:click={playPrev}
          alt='Previous'
          icon='iconoir:skip-prev-solid'
          ControlButton
        />

        <PlayerButton
          on:click={toggleMusic}
          alt={isPlay ? 'Pause' : 'Play'}
          icon={isPlay ? 'iconoir:pause-solid' : 'iconoir:play-solid'}
          ControlButton
          PrimaryButton
        />

        <PlayerButton
          on:click={playNext}
          alt='Next'
          icon='iconoir:skip-next-solid'
          ControlButton
        />
      {/key}
    </div>

    <PlayerRanges
      name='length'
      width='550px'
      value={lengthBar}
      on:click={seekLength}
      on:mousedown={(event) => handleDrag(event, 'length')}
    />
  </div>

  <div class="player-area">
    <div class="player-area-1">
      {#if $hash}
        <AlbumCover
          src={$album === 'Unknown Album'
            ? getArtwork($hash, 128) : getArtwork($albumhash, 128)
          }
          width=56
          height=56
          alt="Front Cover"
        />

        <div class="player-track">
          <ContentHead head='{$title ? $title : ""}' />
          <ContentBody body='{$artist} - {$album}' />
          <!-- 여기 링크 처리 필요한데 컴포넌트로 묶으면 안됨; -->
          <ContentBody body='{convertDateTime(current)} / {convertDateTime(length)}' />
        </div>
      {/if}
    </div>

    <div class="player-area-2">
      <div class="player-volume">
        {#key muteMusic}
          <PlayerRanges
            name='volume'
            width='110px'
            value={musicItem.muted ? 0 : volumeBar}
            on:click={seekVolume}
            on:mousedown={(event) => handleDrag(event, "volume")}
          />

          <PlayerButton
            on:click={muteMusic}
            alt="Volume"
            icon={volumeBar === 0 || musicItem.muted
              ? 'iconoir:sound-off' : volumeBar < 50
              ? 'iconoir:sound-low' : 'iconoir:sound-high'
            }
            off={volumeBar === 0 || musicItem.muted}
          />
        {/key}
      </div>

      <PlayerButton
        on:click={loopMusic}
        alt={isLoop === 2 ? 'Repeat one' : 'Repeat'}
        icon={isLoop === 1
          ? 'iconoir:repeat' : isLoop === 2
          ? 'iconoir:repeat-once' : 'iconoir:repeat'
        }
        off={!isLoop}
      />

      <PlayerButton
        alt='Shuffle'
        icon='iconoir:shuffle'
        off
      />

      <PlayerButton
        alt='Playlist'
        icon='iconoir:playlist'
      />
    </div>
  </div>
</div>

<style>
  .player {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    bottom: 0;
    z-index: 2;
    width: 100%;
    height: 96px;
    background-color: var(--color-dark-bg-trk);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    backdrop-filter: blur(64px);
  }

  .player-area {
    width: 100%;
    display: flex;
    padding: 0 21px;
    justify-content: space-between;
  }

  .player-area-1 {
    display: flex;
    align-items: center;
    gap: var(--app-padding-s);
  }

  .player-area-2 {
    display: flex;
    align-items: center;
  }

  .player-track {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    line-height: 115%;
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-button {
    display: flex;
    justify-content: center;
    padding: 0 6px;
    padding-top: 3px;
    padding-bottom: 2px;
    gap: 24px;
  }

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style>
import { writable, type Writable } from 'svelte/store';

export const hash: Writable<string> = writable('');
export const title: Writable<string> = writable('');
export const album: Writable<string> = writable('Unknown Album');
export const artist: Writable<string> = writable('Unknown Artist');
export const albumhash: Writable<string> = writable('');
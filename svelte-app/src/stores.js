import { writable } from 'svelte/store';

export const user = writable(null); // This will store user data if logged in

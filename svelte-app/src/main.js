import axios from 'axios';
import App from './App.svelte';

// Your remaining code...

const app = new App({
	target: document.body,
	props: {
		name: 'world'
	}
});

export default app;
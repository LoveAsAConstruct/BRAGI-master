<script>
	import Router from 'svelte-spa-router';
	import Home from './routes/Home.svelte';
	import Login from './routes/Login.svelte';
	import Register from './routes/Register.svelte';
	import Navbar from './components/Navbar.svelte';
  </script>
  <Navbar/>
  <Router>
	<Home path="/" />
	<Login path="/login" />
	<Register path="/register" />
  </Router>
  
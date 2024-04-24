<script>
    import { Router, Route } from 'svelte-routing';
    import Home from './components/Home.svelte';
    import Login from './components/Login.svelte';
    import Profile from './components/Profile.svelte';
    import Stats from './components/Stats.svelte';
</script>

<Navbar />

<Router>
    <Route path="/" component={Home} />
    <Route path="/login" component={Login} />
    <Route path="/profile" component={Profile} />
    <Route path="/stats" component={Stats} />
</Router>

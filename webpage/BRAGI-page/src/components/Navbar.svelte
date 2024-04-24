<script>
    import { onMount } from 'svelte';
    let loggedIn = false;

    onMount(() => {
        // Check if user is logged in (simple simulation)
        loggedIn = !!localStorage.getItem('user');
    });
</script>

<nav style="background-color: #333; color: white; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
    <div>Logo</div>
    <div>
        {#if loggedIn}
            <a href="/profile">Profile</a>
            <a href="/stats">Stats</a>
        {:else}
            <a href="/login">Log In</a>
            <a href="/signin">Sign In</a>
        {/if}
    </div>
</nav>

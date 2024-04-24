<!-- LoginForm.svelte -->

<script>
    let username = '';
    let password = '';

    function login() {
        // Implement login functionality here
        // For demonstration purposes, let's assume the login is successful
        console.log('Logging in...');
    }
</script>

<main>
    <!-- Login Form -->
    <form on:submit|preventDefault="{login}">
        <label>
            Username:
            <input type="text" bind:value="{username}">
        </label>
        <label>
            Password:
            <input type="password" bind:value="{password}">
        </label>
        <button type="submit">Login</button>
    </form>
</main>

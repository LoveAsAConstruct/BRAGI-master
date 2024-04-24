<!-- Navbar.svelte -->

<script>
    let loggedIn = false;
    let username = '';

    function logout() {
        // Implement logout functionality here
        loggedIn = false;
        username = '';
    }
</script>

<style>
    /* Styles for the Navbar component */
    nav {
        background-color: #222;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    nav ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        display: flex;
    }

    nav ul li {
        margin-right: 20px;
    }

    nav ul li:last-child {
        margin-right: 0;
    }

    nav ul li a {
        color: #fff;
        text-decoration: none;
        padding: 5px 10px;
        border-radius: 5px;
    }

    .profile-tab {
        display: flex;
        align-items: center;
    }

    .profile-tab span {
        margin-right: 10px;
    }
</style>

<nav>
    <div>
        <h1>Your App Name</h1>
    </div>
    <div>
        <ul>
            {#if !loggedIn}
                <li><a href="#">Login / Sign Up</a></li>
            {:else}
                <li><a href="#">Profile</a></li>
                <li><a href="#">Stats</a></li>
                <li class="profile-tab">
                    <span>Welcome, {username}!</span>
                    <button on:click="{logout}">Logout</button>
                </li>
            {/if}
        </ul>
    </div>
</nav>

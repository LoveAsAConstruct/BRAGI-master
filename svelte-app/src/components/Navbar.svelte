<script>
  import { link } from 'svelte-spa-router';
</script>

<nav>
  <a use:link href="/">Home</a>
  <a use:link href="/login">Login</a>
  <a use:link href="/register">Register</a>
</nav>

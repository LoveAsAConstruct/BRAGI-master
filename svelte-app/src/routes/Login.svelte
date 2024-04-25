<script>
    import axios from 'axios';
  
    let username = '';
    let password = '';
  
    async function login() {
      try {
        const response = await axios.post('http://localhost:3001/login', { username, password });
        console.log('Login successful', response.data);
        // Handle successful login, e.g., redirect or store user info
      } catch (error) {
        console.error('Login failed', error.response.data);
      }
    }
  </script>
  
  <form on:submit|preventDefault={login}>
    <input placeholder="Username" bind:value={username} />
    <input type="password" placeholder="Password" bind:value={password} />
    <button type="submit">Login</button>
  </form>
  
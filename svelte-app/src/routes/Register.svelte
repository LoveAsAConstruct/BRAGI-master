<script>
    import axios from 'axios';
    let username = '';
    let password = '';
  
    async function register() {
      try {
        const response = await axios.post('http://localhost:3001/register', { username, password });
        console.log('Registration successful', response.data);
        // Redirect or notify user
      } catch (error) {
        console.error('Registration failed', error.response.data);
      }
    }
  </script>
  
  <form on:submit|preventDefault={register}>
    <input placeholder="Username" bind:value={username} />
    <input type="password" placeholder="Password" bind:value={password} />
    <button type="submit">Register</button>
  </form>
  
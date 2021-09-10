<template>
  <main class="form">
    <form @submit.prevent="onSubmit">
      <h1 class="h3 mb-3 fw-normal">Logi sisse</h1>
      <div class="form-floating">
        <input type="text" v-model="username" class="form-control" id="username" placeholder="Kasutajatunnus">
        <label for="username">Kasutajatunnus</label>
      </div>
      <div class="form-floating">
        <input type="password" v-model="password" class="form-control" id="password" placeholder="Parool">
        <label for="password">Parool</label>
      </div>
      <button class="w-100 btn btn-lg btn-primary" type="submit">Logi sisse</button>
    </form>
  </main>
  <p>Pole veel kasutajat? <router-link to="/register">Registreeru</router-link></p>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async onSubmit() {

      if (!this.username) {
        document.getElementById('username').className += ' is-invalid';
        document.getElementById('password').className += ' is-invalid';
        return
      } else {
        document.getElementById('username').className = 'form-control';
      }

      if (!this.password) {
        document.getElementById('password').className += ' is-invalid';
        return
      } else {
        document.getElementById('password').className = 'form-control';
      }

      try {
        const res = await axios.post('login', {
          username: this.username,
          password: this.password
        })
        if (res.status === 200) {
          localStorage.setItem('token', res.data.access_token);
          localStorage.setItem('role', res.data.role);
          axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.access_token;
          this.$router.push('/');
        }
      } catch {
        document.getElementById('username').className += ' is-invalid';
        document.getElementById('password').className += ' is-invalid';
      }

      this.username = '';
      this.password = '';
    }
  }
}
</script>
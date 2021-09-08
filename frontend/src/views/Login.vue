<template>
  <main class="form-signin">
    <form @submit.prevent="onSubmit">
      <h1 class="h3 mb-3 fw-normal">Logi sisse</h1>
      <div class="form-floating">
        <input type="username" v-model="username" class="form-control" id="username" placeholder="Kasutajatunnus">
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
import axios from "axios";

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
        alert('Sisesta kasutajanimi')
        return
      }

      if (!this.password) {
        alert('Sisesta parool')
        return
      }

      const res = await axios.post('http://localhost:5000/login', {
        username: this.username,
        password: this.password
      })

      if (res.status === 200) {
        localStorage.setItem('token', res.data.access_token)
        localStorage.setItem('role', res.data.role)
        this.$router.push('/')
      }

      this.username = ''
      this.password = ''
    }
  }
}
</script>
<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}
</style>
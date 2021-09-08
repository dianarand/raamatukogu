<template>
  <main class="form">
    <form @submit.prevent="onSubmit">
      <h1 class="h3 mb-3 fw-normal">Registreeru</h1>
      <div class="form-floating">
        <input type="text" v-model="username" class="form-control" id="username" placeholder="Kasutajatunnus">
        <label for="username">Kasutajatunnus</label>
      </div>
      <div class="form-floating">
        <input type="password" v-model="password" class="form-control" id="password" placeholder="Parool">
        <label for="password">Parool</label>
      </div>
      <div class="text-start" id="role-selection">
        <label>Soovin:</label>
        <div class="form-check">
          <input class="form-check-input" type="radio" v-model="role" name="role" id="borrower">
          <label class="form-check-label" for="borrower">
            Laenata raamatuid
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" v-model="role" name="role" id="lender">
          <label class="form-check-label" for="lender">
            Laenutada välja oma raamatuid
          </label>
        </div>
      </div>
      <button class="w-100 btn btn-lg btn-primary" type="submit">Registreeru</button>
    </form>
  </main>
  <p>Kasutaja olemas? <router-link to="/login">Logi sisse</router-link></p>
</template>

<script>
import axios from "axios";

export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      role: '',
    }
  },
  methods: {
    async onSubmit() {
      if(!this.username) {
        alert('Sisesta kasutajanimi')
        return
      }

      if(!this.password) {
        alert('Sisesta parool')
        return
      }

      const res = await axios.post('register', {
        username: this.username,
        password: this.password,
        role: this.role
      })

      this.username = ''
      this.password = ''

      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
#role-selection {
  padding: 5px 10px 20px 10px;
  margin-top: 5px;
}
</style>
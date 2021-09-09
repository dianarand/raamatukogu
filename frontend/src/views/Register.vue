<template>
  <main class="form">
    <div class="alert alert-warning" role="alert" v-if="msg !== ''">
      {{ msg }}
      <button type="button" class="btn-close btn-sm float-end" @click="clearMessage"></button>
    </div>
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
          <input class="form-check-input" type="radio" v-model="role" value="borrower" name="role" id="borrower">
          <label class="form-check-label" for="borrower">
            Laenata raamatuid
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" v-model="role" value="lender" name="role" id="lender">
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
      msg: ''
    }
  },
  methods: {
    async onSubmit() {
      if (!this.username) {
        document.getElementById('username').className += " is-invalid"
        document.getElementById('password').className += " is-invalid"
        return
      } else {
        document.getElementById('username').className = "form-control"
      }

      if (!this.password) {
        document.getElementById('password').className += " is-invalid"
        return
      } else {
        document.getElementById('password').className = "form-control"
      }

      if (!this.role) {
        this.setMessage("Rolli valik on kohustuslik")
        return
      }

      try {
        const res = await axios.post('register', {
          username: this.username,
          password: this.password,
          role: this.role
        })
        if (res.status === 201) {
          this.$router.push('/login');
        }
      } catch(err) {
        this.setMessage(err.response.data.message)
      }

      this.username = ''
      this.password = ''
    },
    setMessage(message) {
      this.msg = message
    },
    clearMessage() {
      this.msg = ''
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
<template>
  <div class="container">
    <div class="header">
      <h2>Logi sisse</h2>
    </div>
    <form @submit.prevent="onSubmit" class="add-form">
      <div class="form-control">
        <label>Kasutajatunnus</label>
        <input type="text" v-model="username" name="username" placeholder="Kasutajatunnus" />
      </div>
      <div class="form-control">
        <label>Parool</label>
        <input type="password" v-model="password" name="password" placeholder="Parool" />
      </div>
      <input type="submit" value="Logi sisse" class="btn btn-block" />
    </form>
    <p>Pole veel kasutajat?</p>
    <h3><router-link to="/register">Registreeru</router-link></h3>
  </div>
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
      }

      this.username = ''
      this.password = ''

      console.log(localStorage.getItem('token'))

      this.$router.push('/')
    }
  }
}
</script>
<style scoped>
.add-form {
  margin-bottom: 40px;
}
.form-control {
  margin: 20px 0;
}
.form-control label {
  display: block;
}
.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px;
  padding: 3px 7px;
  font-size: 17px;
}
.form-control-check label {
  flex: 1;
}
.form-control-check input {
  flex: 2;
  height: 20px;
}
</style>
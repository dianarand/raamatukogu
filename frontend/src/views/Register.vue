<template>
  <div class="container">
    <div class="header">
      <h2>Registreeru</h2>
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
      <div class="form-control">
        <label>Soovin</label>
        <input type="radio" id="lender" name="role" value="lender" v-model="role">
        <label for="lender">Laenutada välja oma raamatuid</label>
        <input type="radio" id="borrower" name="role" value="borrower" v-model="role">
        <label for="borrower">Laenata raamatuid</label>
      </div>
      <input type="submit" value="Registreeru" class="btn btn-block" />
    </form>
    <p>Kasutaja olemas?</p>
    <h3><router-link to="/login">Logi sisse</router-link></h3>
  </div>
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
      console.log(res.data.message)

      this.username = ''
      this.password = ''

      this.$router.push('/login')
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

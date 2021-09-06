<template>
  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>Kasutajatunnus</label>
      <input type="text" v-model="username" name="username" placeholder="Kasutajatunnus" />
    </div>
    <div class="form-control">
      <label>Parool</label>
      <input type="text" v-model="password" name="password" placeholder="Parool" />
    </div>
    <input type="submit" value="Logi sisse" class="btn btn-block" />
  </form>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      access_token: undefined,
    }
  },
  methods: {
    ...mapActions(['logIn']),
    onSubmit(e) {
      e.preventDefault()

      if(!this.username) {
        alert('Sisesta kasutajanimi')
        return
      }

      if(!this.password) {
        alert('Sisesta parool')
        return
      }

      const user = {
        username: this.username,
        password: this.password
      }

      this.logIn(user)

      this.username = ''
      this.password = ''

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

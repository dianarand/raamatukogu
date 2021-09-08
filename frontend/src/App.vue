<template>
  <header>
    <h1>Raamatute laenutus</h1>
  </header>
  <router-view></router-view>
</template>

<script>
import Box from './components/Books'

export default {
  name: 'App',
  components: {
    Box
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
    checkCredentials() {
      if (localStorage.getItem('token') === null) {
        this.$router.push('/login')
      }
    }
  },
  created() {
    this.checkCredentials()
  }
}
</script>
<style>
.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>

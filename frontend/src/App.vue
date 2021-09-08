<template>
  <Header />
  <router-view></router-view>
</template>

<script>
import Header from './components/Header'

export default {
  name: 'App',
  components: {
    Header
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
.form {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form .form-floating:focus-within {
  z-index: 2;
}

.form input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>

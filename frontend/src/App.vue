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

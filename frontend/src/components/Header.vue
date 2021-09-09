<template>
  <div class="container">
    <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
      <router-link to="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
        <span class="fs-4">Raamatute laenutus</span>
      </router-link>
      <ul class="nav nav-pills">
        <li v-if="isLoggedIn" class="nav-item">
          <a href="javascript:void(0)" class="nav-link" @click="logOut">Logi välja</a>
        </li>
      </ul>
    </header>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Header",
  computed: {
    isLoggedIn() {
      const token = localStorage.getItem('token')
      if (token !== null && token !== undefined) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    logOut() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      axios.defaults.headers.common['Authorization'] = null;
      this.$router.push('/login')
    },
  }
}
</script>

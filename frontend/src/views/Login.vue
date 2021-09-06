<template>
  <div class="container">
    <div class="header">
      <LogIn @user-login="logIn"/>
    </div>
  </div>
</template>

<script>
import LogIn from '../components/LogIn'

export default {
  name: 'Login',
  components: {
    LogIn
  },
  methods: {
    logIn(access_token) {
      this.$emit('user-login', access_token)
      this.$router.push('/')
    }
  },
}
</script>
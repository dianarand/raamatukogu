<template>
  <div class="container">
    <div class="header">
      <LogIn />
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
  emits: ['access_token']
}
</script>
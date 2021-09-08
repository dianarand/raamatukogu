<template>
  <button @click=onClick() class="btn btn-primary">{{ text }}</button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    text: String,
    color: String
  },
  methods: {
     onClick () {
       this.$emit('btn-click')
     }
  }
}
</script>
<style>
button {
  width: 125px;
}
</style>
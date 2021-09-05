<template>
  <header>
    <h1>{{ title }}</h1>
    <Button
        @btn-click="$emit('toggle-add-book')"
        :text="showAddBook ? 'Sulge' : 'Lisa raamat'"
        :color="showAddBook ? 'red' : 'green'"/>
  </header>
</template>

<script>
import Button from './Button'

  export default {
    name: 'Header',
    props: {
      title: String,
      showAddBook: Boolean,
    },
    components: {
      Button
    }
  }
</script>

<style scoped>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
</style>
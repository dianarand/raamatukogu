<template>
  <header>
    <h1>Raamatute laenutus</h1>
  </header>
  <p>{{ msg }}</p>
  <router-view></router-view>
</template>

<script>
import Box from './components/Box'

export default {
  name: 'App',
  components: {
    Box
  },
  data() {
    return {
      msg: ''
    }
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap');
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  font-family: 'Poppins', sans-serif;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.container {
  max-width: 800px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 1px solid steelblue;
  padding: 30px;
  border-radius: 5px;
}
.btn {
  display: inline-block;
  background: #000;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
}
.btn:focus {
  outline: none;
}
.btn:active {
  transform: scale(0.98);
}
.btn-block {
  display: block;
  width: 100%;
}
</style>

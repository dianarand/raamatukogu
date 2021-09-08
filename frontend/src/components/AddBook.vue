<template>
  <main class="form">
    <form @submit.prevent="onSubmit">
      <h1 class="h3 mb-3 fw-normal">Lisa uus raamat</h1>
      <div class="form-floating">
        <input type="text" v-model="title" class="form-control" id="title" placeholder="Pealkiri">
        <label for="title">Pealkiri</label>
      </div>
      <div class="form-floating">
        <input type="text" v-model="author" class="form-control" id="author" placeholder="Autor">
        <label for="author">Autor</label>
      </div>
      <div class="form-floating">
        <input type="number" min="1700" max="2050" v-model="year" class="form-control" id="year" placeholder="Ilmumisaasta">
        <label for="author">Ilmumisaasta</label>
      </div>
      <button class="w-100 btn btn-lg btn-primary" type="submit">Salvesta raamat</button>
    </form>
  </main>
</template>
<script>
import axios from "axios";

export default {
  name: 'AddBook',
  data() {
    return {
      title: '',
      author: '',
      year: ''
    }
  },
  methods: {
    async onSubmit() {
      if(!this.title) {
        alert('Palun lisa pealkiri')
        return
      }

      if(!this.author) {
        alert('Palun lisa autor')
        return
      }

      if(!this.year) {
        alert('Palun lisa ilmumisaasta')
        return
      }

      const book = {
        title: this.title,
        author: this.author,
        year: this.year
      }

      const res = await axios.post('books', book)

      this.$emit('setMessage', res)

      if (res.status === 201) {
        this.$emit('addBook', book)
      }

      this.title = ''
      this.author = ''
      this.year = ''

      this.$emit('hideAddBook')
    },
  }
}
</script>
<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form input[type="number"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
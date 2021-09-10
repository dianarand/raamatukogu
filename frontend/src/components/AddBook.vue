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
import axios from 'axios';

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
      if (!this.title) {
        document.getElementById('title').className += ' is-invalid';
      } else {
        document.getElementById('title').className = 'form-control';
      }

      if (!this.author) {
        document.getElementById('author').className += ' is-invalid';
      } else {
        document.getElementById('author').className = 'form-control';
      }

      if (!this.year) {
        document.getElementById('year').className += ' is-invalid';
      } else {
        document.getElementById('year').className = 'form-control';
      }

      if (!this.title || !this.author || !this.year) {
        return;
      }

      const book = {
        title: this.title,
        author: this.author,
        year: this.year
      }

      try {
        const res = await axios.post('books', book);
        this.$emit('setMessage', res);
        if (res.status === 201) {
          this.$emit('addBook', res.data.id)
          this.title = ''
          this.author = ''
          this.year = ''
          this.$emit('hideAddBook')
        }
      } catch(err) {
        this.$emit('setMessage', err.response);
      }
    },
  }
}
</script>
<style scoped>
.form input[type="number"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
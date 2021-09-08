<template>
  <form @submit.prevent="onSubmit" class="add-form">
    <div class="form-control">
      <label>Pealkiri</label>
      <input type="text" v-model="title" name="title" placeholder="Lisa raamat" />
    </div>
    <div class="form-control">
      <label>Autor</label>
      <input type="text" v-model="author" name="autor" placeholder="Lisa autor" />
    </div>
    <div class="form-control">
      <label>Ilmumisaasta</label>
      <input type="text" v-model="year" name="year" placeholder="Lisa ilmumisaasta" />
    </div>
    <input type="submit" value="Salvesta raamat" class="btn btn-block" />
  </form>
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

      this.$emit('setMessage', res.data.message)

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
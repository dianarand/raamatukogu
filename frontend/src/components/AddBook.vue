<template>
  <form @submit="onSubmit" class="add-form">
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
import { mapActions } from 'vuex'

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
    ...mapActions(['addBook']),
    onSubmit(e) {
      e.preventDefault()

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

      const newBook = {
        title: this.title,
        author: this.author,
        year: this.year,
      }

      this.addBook(newBook)

      this.title = ''
      this.author = ''
      this.year = ''

      this.$emit('hideAddBook')
    }
  }
}
</script>

<style scoped>
.add-form {
  margin-bottom: 40px;
}
.form-control {
  margin: 20px 0;
}
.form-control label {
  display: block;
}
.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px;
  padding: 3px 7px;
  font-size: 17px;
}
.form-control-check label {
  flex: 1;
}
.form-control-check input {
  flex: 2;
  height: 20px;
}
</style>

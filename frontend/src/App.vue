<template>
  <div class="container">
    <Header @toggle-add-book="toggleAddBook" title="Raamatud" :showAddBook="showAddBook"/>
    <div v-show="showAddBook">
      <AddBook @add-book="addBook"/>
    </div>
    <Books @delete-book="deleteBook" :books="books"/>
  </div>
</template>

<script>
import Header from './components/Header'
import Books from './components/Books'
import AddBook from './components/AddBook'

export default {
  name: 'App',
  components: {
    Header,
    Books,
    AddBook
  },
  data() {
    return {
      books: [],
      showAddBook: false
    }
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
    addBook(book) {
      this.books = [...this.books, book]
    },
    deleteBook(id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        this.books = this.books.filter((book) => book.id != id)
      }
    },
  },
  created() {
    this.books = [
      {
        id: 1,
        title: "Harry Potter and the Philosopher's Stone",
        author: "J. K. Rowling",
        year: "1997",
        active: true,
        reminder: true,
      },
      {
        id: 2,
        title: "Hunger Games",
        author: "Suzanne Collins",
        year: "2008",
        active: true,
        reminder: true,
      },
      {
        id: 3,
        title: "A Court of Thorns and Roses",
        author: "Sarah J. Maas",
        year: "2015",
        active: true,
        reminder: false,
      }
    ]
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
.container {
  max-width: 500px;
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

<template>
  <div class="container">
    <p>{{ msg }}</p>
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
import axios from 'axios';

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
      showAddBook: false,
      msg: ''
    }
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
    addBook(book) {
      const payload = {
        title: book.title,
        author: book.author,
        year: book.year
      }
      const path = 'http://localhost:5000/books'
      axios.post(path, payload)
      .then ((res) => {
        this.msg = res.data['message']
      })
      .catch ((err) => {
        console.error(err);
      });
      this.books = [...this.books, book]
    },
    deleteBook(id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        const path = `http://localhost:5000/book/${id}`
        console.log(path)
        axios.delete(path)
            .then((res) => {
              if (res.status === 200) {
                this.books = this.books.filter((book) => book.id != id)
              }
              this.msg = res.data['message']
            })
            .catch((err) => {
              console.error(err);
            });
      }
    },
    fetchBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
      .then ((res) => {
        this.books = res.data['books'];
      })
      .catch ((err) => {
        console.error(err);
      });
    },
  },
  created() {
    this.fetchBooks();
  },
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

<template>
  <div class="book">
    <h3>
      {{ book.title }}
      <div role="group">
        <i class="fas fa-undo-alt"></i>
        <i class="fas fa-chevron-down"></i>
        <i @click="$emit('remove-book', book.id)" class="fas fa-times"></i>
      </div>
    </h3>
    <p>{{ book.author }} ({{ book.year }})</p>
  </div>
</template>

<script>
export default {
  name: 'Book',
  props: {
    book: Object
  },
}
</script>

<style scope>
.fas {
  color: red;
}
.book {
  background: #f4f4f4;
  margin: 5px;
  padding: 10px 20px;
  cursor: pointer;
}
.book h3 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
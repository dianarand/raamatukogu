<template>
<nav aria-label="Page navigation example">
  <ul class="pagination justify-content-center py-3">
    <li class="page-item">
      <a class="page-link" href="javascript:void(0)" @click="$emit('previousPage')" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
    <li class="page-item">
      <a class="page-link" href="javascript:void(0)" @click="$emit('nextPage')" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
</template>

<script>
export default {
  name: "Pagination"
}
</script>

<style scoped>
a {
  color: black;
}
</style>
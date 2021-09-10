<template>
  <nav>
    <ul class="pagination justify-content-center py-3">
      <li class="page-item">
        <a class="page-link" href="javascript:void(0)" @click="$emit('previousPage')">
          <span>&laquo;</span>
        </a>
      </li>
      <li class="page-item">
        <a class="page-link" href="javascript:void(0)" @click="$emit('nextPage')">
          <span>&raquo;</span>
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
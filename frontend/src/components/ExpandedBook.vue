<template>
  <div>
    <hr>
    <div v-bind:class="alert" role="alert" v-if="msg !== ''">
      {{ msg }}
    </div>
    <div v-show="bookIsOut">
      <p>Raamat on välja laenutatud.</p>
      <div v-if="showAdditional">
        <p>Laenutuse tähtaeg: {{ book.deadline }}</p>
        <a href="javascript:void(0)" @click="returnBook(book.id)">Märgi tagastatuks</a>
      </div>
    </div>
    <div v-show="bookIsReserved">
      <p>Raamat on broneeritud.</p>
      <div v-if="showAdditional">
        <a href="javascript:void(0)" @click="cancelReservation(book.id)">Tühista broneering</a>
      </div>
    </div>
    <div v-show="!bookIsOut && !bookIsReserved">
      <a href="javascript:void(0)"
         @click="lendBook(book.id)"
         v-if="showForLender">Märgi raamat laenutatuks</a>
      <a href="javascript:void(0)"
         @click="borrowBook(book.id)"
         v-if="showForBorrower">Laenuta raamat</a><br>
      <a href="javascript:void(0)"
         @click="reserveBook(book.id)"
         v-if="showForBorrower">Broneeri raamat</a>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {showForLender, showForBorrower, alertClass} from "../utils";

export default {
  name: 'ExpandedBook',
  data() {
    return {
      msg: '',
      alert: "alert alert-primary"
    }
  },
  props: {
    book: Object,
    showAdditional: Boolean
  },
  computed: {
    bookIsOut() {
      if (this.book.lending === undefined) {
        return false
      } else if (this.book.lending !== null) {
        return true
      } else {
        return false
      }
    },
    bookIsReserved() {
      if (this.book.reservation === undefined) {
        return false
      } else if (this.book.reservation !== null) {
        return true
      } else {
        return false
      }
    },
    showForLender,
    showForBorrower
  },
  methods: {
    async lendBook(id) {
      const borrower = prompt('Millisele kasutajale laenutad raamatu?', 'kasutajanimi')
      const res = await axios.post(`book/${id}/lend`, {'borrower': borrower})
      if (res.status === 200) {
          this.book.lending = res.data.user
          this.book.deadline = res.data.deadline
        }
      this.alert = alertClass(res.status)
      this.msg = res.data.message
    },
    async borrowBook(id) {
      const res = await axios.post(`book/${id}/borrow`)
      if (res.status === 200) {
        this.book.lending = res.data.user
        this.book.deadline = res.data.deadline
      }
      this.alert = alertClass(res.status)
      this.msg = res.data.message
    },
    async reserveBook(id) {
      const res = await axios.post(`book/${id}/reserve`)
      if (res.status === 200) {
        this.book.reservation = res.data.user
      }
      this.alert = alertClass(res.status)
      this.msg = res.data.message
    },
    async returnBook(id) {
      const res = await axios.post(`book/${id}/return`)
      if (res.status === 200) {
          this.book.lending = null
        }
      this.alert = alertClass(res.status)
      this.msg = res.data.message
    },
    async cancelReservation(id) {
      const res = await axios.post(`book/${id}/cancel`)
      if (res.status === 200) {
          this.book.reservation = null
        }
      this.alert = alertClass(res.status)
      this.msg = res.data.message
    },
  }
}
</script>
<style scoped>
.alert {
  width: 100%;
  margin: 15px 0px;
}
</style>
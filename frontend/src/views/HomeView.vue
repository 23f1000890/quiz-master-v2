<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const message = ref([])

const fetchdata = async () => {
  const response = await fetch('http://127.0.0.1:4001/')
  message.value = await response.json()
}
fetchdata()

const router = useRouter()

const navigateTo = (role) => {
  const token = localStorage.getItem('access_token')
  const sharedRole = localStorage.getItem('role')

  if (token && sharedRole === role) {
    router.push(`/${role}`)
  } else {
    router.push(`/login`)
  }
}
</script>

<template>
  <div class="wrapper">
    <img src="/intelliquest.png" alt="logo" />
    <h1 class="heading">{{ message.msg }}</h1>
    <div class="d-inline-flex gap-1">
      <button
        class="btn btn-dark"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#collapseExample"
      >
        Know More
      </button>
      <br />
    </div>
    <div class="collapse" id="collapseExample">
      <div class="card card-body d-flex flex-wrap">
        {{ message.desc }}
      </div>
    </div>
    <div class="gap-2 mt-3 mb-3" style="display: flex; justify-content: center">
      <button @click="navigateTo('admin')" class="btn btn-dark">Admin</button>
      <button @click="navigateTo('user')" class="btn btn-dark">User</button>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  padding: 5rem;
  text-align: center;
  color: beige;
  margin: 10% auto;
}
.heading {
  font-size: 5rem;
}
.heading:hover {
  color: #de467b;
}
.card {
  color: #de467b;
  background-color: #141005;
}
.btn {
  background-color: #141005;
  border-color: #de467b;
}
</style>

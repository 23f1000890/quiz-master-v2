<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()

const isLoggedIn = computed(() => localStorage.getItem('access_token'));

const logout = async () => {
  try {
    const result = await fetch('http://127.0.0.1:4001/auth/logout/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    })
    if (result.ok) {
      localStorage.clear()
      router.push('/login')
    }
  } catch (err) {
    console.error(err)
    alert('logout Failed!!!')
  }
}
</script>

<template>
  <nav class="navbar bg-danger-subtle sticky-top border-bottom" data-bs-theme="dark">
    <div class="container-fluid">
      <router-link to="/" class="wrapper navbar-brand">
        <img src="/intelliquest.png" alt="logo" height="50" width="50" />
        Intelliquest 2.0
      </router-link>
      <div class="navbar-brand ms-auto gap-3 d-flex">
        <router-link to="/" class="btn btn-light nav-link">Home</router-link>
        <router-link to="/login" v-if="!isLoggedIn" class="btn btn-light nav-link"
          >login</router-link
        >
        <button v-else @click="logout" class="btn btn-light nav-link">logout</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.wrapper {
  color: white;
  cursor: pointer;
}
</style>

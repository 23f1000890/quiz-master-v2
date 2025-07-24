<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const message = ref([]);
const route = useRoute();
const success = ref("");

const fetchdata = async() => {
    const token = localStorage.getItem('access_token');

    const res = await fetch("http://127.0.0.1:4001/user/", {
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    })
    message.value = await res.json();
}

onMounted(() => {
    if(route.query.flash) {
        success.value = route.query.flash //read flash message from the route
    }
})

fetchdata();
</script>

<template>
    <div class="alert alert-success alert-dismissible fade show col-4 offset-8 mt-3" v-if="success" role="alert">
      {{ success }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <h1 class="text-danger">Hello User</h1>
</template>
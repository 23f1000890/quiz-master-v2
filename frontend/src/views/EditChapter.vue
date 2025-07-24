<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const chapter_id = route.params.chapter_id;
const chapter_name = ref(route.query.chapter_name || "");
const description = ref(route.query.description || "");
const error = ref("");

const handleSubmit = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:4001/admin/edit_chapter/${chapter_id}/`, {
            method: 'PUT',
            headers: {
                'content-type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify({
                chapter_name: chapter_name.value, 
                description: description.value,
            }),
        })

        const message = await response.json();
        if(!response.ok) {
            error.value = message.msg || "Updates went wrong!";
        } else {
            router.push({
                path: '/admin',
                query: { flash: message.msg || 'Chapter Updated Successfully'}
            })
        }
    } catch(err) {
        error.value = err.message;
    }
}
</script>

<template>
    <div class="container mt-5 form-body row-gap-3 col-6 offset-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <h1 class="text-light border-3 border-bottom border-danger-subtle mb-4 mt-3 text-center">Update The Chapter</h1>
        <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
            {{ error }}
            <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <form @submit.prevent="handleSubmit">
            <div class="mb-3 col-12">
                <label for="chapter_name" class="form-label">Name of the Chapter:</label>
                <input type="text" v-model="chapter_name" name="chapter_name" id="chapter_name" class="form-control">
            </div>
            <div class="mb-3 col-12">
                <label for="description" class="form-label">Chapter Summary:</label>
                <textarea name="description" v-model="description" id="description" class="form-control"></textarea>
            </div>
            <button type="submit" class="btn btn-success mt-3">Update</button>
            <router-link to="/admin" class="btn btn-danger mt-3 ms-3">Cancel</router-link>
        </form>
    </div>
</template>

<style scoped>
.form-label {
  color: greenyellow;
}
.form-control {
  border-color: greenyellow;
}
.btn-link {
  text-decoration: none;
  font-weight: 700;
  font-size: 2rem;
}
</style>
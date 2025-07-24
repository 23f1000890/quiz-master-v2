<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const subject_id = route.params.subject_id;
const subject_name = ref(route.query.subject_name || "");
const description = ref(route.query.description || "");
const error = ref("");

const handleSubmit = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:4001/admin/edit_subject/${subject_id}/`, {
            method: 'PUT',
            headers: {
                'content-type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify({
                subject_name: subject_name.value, 
                description: description.value,
            }),
        })

        const message = await response.json();
        if(!response.ok) {
            error.value = message.msg || "Updates went horribly wrong!";
        } else {
            router.push({
                path: '/admin',
                query: { flash: message.msg || 'Subject Updates Successfully'}
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
        <h1 class="text-light border-3 border-bottom border-danger-subtle mb-4 mt-3 text-center">Update Subject</h1>
        <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
            {{ error }}
            <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <form @submit.prevent="handleSubmit">
            <div class="mb-3 col-12">
                <label for="subject_name" class="form-label">Name of the Subject:</label>
                <input type="text" v-model="subject_name" name="subject_name" id="subject_name" class="form-control" placeholder="Edit subject">
            </div>
            <div class="mb-3 col-12">
                <label for="description" class="form-label">Description:</label>
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
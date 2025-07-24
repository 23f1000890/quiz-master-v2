<script setup>
import { ref } from 'vue';

const message = ref([]);
const success = ref("");

const fetchdata = async() => {
    const res = await fetch("http://127.0.0.1:4001/admin/user_details/", {
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        }
    })
    message.value = await res.json();
}

const DetailsDelete = async(user_id) => {
    // Remove users from the list
    message.value.users = message.value.users.filter(user => user.user_id !== user_id);

    // Show flash message without page reload
    success.value = "Subject Deleted Successfully!";
}
fetchdata();
</script>

<template>
    <div class="alert alert-success alert-dismissible fade show col-4 offset-8 mt-3" v-if="success" role="alert">
      {{ success }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="container form-body row-gap-3 mt-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <router-link to="/admin" class="btn btn-primary"><strong>Admin Portal</strong></router-link>
        <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">Admin Panel</h1>
        <table class="table table-dark table-bordered border-primary">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Chirantan Chakraborty</td>
                    <td>{{ message.admin_email }}</td>
                    <td>{{ message.admin_role }}</td>
                </tr>
            </tbody>
        </table>
        <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">User Panel</h1>
        <table class="table table-dark table-bordered border-primary mb-5">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Date of Birth</th>
                    <th>Location</th>
                    <th>Qualification</th>
                    <th>Status</th>
                    <th>Role</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in message.users" :key="user.user_id">
                    <td>{{ user.user_id }}</td>
                    <td>{{ user.full_name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.dob }}</td>
                    <td>{{ user.location }}</td>
                    <td>{{ user.qualification }}</td>
                    <td>Active</td>
                    <td>{{ user.user_role }}</td>
                    <td><button @click="DetailsDelete(user.user_id)" class="btn btn-info ms-2">Delete</button></td>
                </tr>
            </tbody>
        </table>
        <router-link to="/login" class="btn btn-warning text-center mb-5 mt-3 col-6 offset-3">+ Add New User</router-link>
    </div>
</template>

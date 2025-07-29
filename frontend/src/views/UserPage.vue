<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const message = ref([]);
const success = ref("");

const user_id = route.params.user_id;

const fetchdata = async() => {
    const res = await fetch(`http://127.0.0.1:4001/user/${user_id}/`, {
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        }
    })
    message.value = await res.json();
}

onMounted(() => {
    if(route.query.flash) {
        success.value = route.query.flash //read flash message from the route
    }
})

// reactively update success on query change
watch(() => route.query.flash, (newVal) => {
  if (newVal) {
    success.value = newVal;
  }
});

fetchdata();
</script>

<template>
    <div class="alert alert-success alert-dismissible fade show col-4 offset-8 mt-3" v-if="success" role="alert">
      {{ success }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="container form-body row-gap-3 mt-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <div class="d-grid d-lg-flex justify-content-lg-end mt-5 gap-2 me-5">
            <router-link :to="{
                path: `/user/${user_id}/summary/`,
            }" class="btn btn-primary"><strong>Summary</strong></router-link>
        </div>
        <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">-- Upcoming Quizzes --</h1>
        <table class="table table-dark table-bordered border-primary">
            <thead>
                <tr>
                    <th>Quiz Tester</th>
                    <th>ID</th>
                    <th>No of Questions</th>
                    <th>Chapter Name</th>
                    <th>Start Date & Time</th>
                    <th>Duration</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody v-for="quiz in message.quizzes" :key="quiz.quiz_id">
                <tr>
                    <td>{{ message.username }}</td>
                    <td>{{ quiz.quiz_id }}</td>
                    <td>{{ quiz.question_count }}</td>
                    <td>{{ quiz.chapter_name }}</td>
                    <td>{{ quiz.start_time }}</td>
                    <td>{{ quiz.time_duration }}</td>
                    <td>
                        <router-link :to="{
                            path: `/user/${user_id}/quiz/${quiz.quiz_id}/start/`,
                            query: {
                                chapter_name: quiz.chapter_name,
                            }
                        }" class="btn btn-success ms-3">Start</router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
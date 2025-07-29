<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const attempts = ref([]);

const summary = async() => {
    const response = await fetch(`http://127.0.0.1:4001/user/${route.params.user_id}/summary/`, {
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`,
        }
    });
    const res = await response.json();
    attempts.value = res.attempts;
}
summary()
</script>

<template>
    <div class="container form-body row-gap-3 mt-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">Evaluation Panel</h1>
        <table class="table table-dark table-bordered border-primary">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Chapter Name</th>
                    <th>Submitted At</th>
                    <th>Time Taken</th>
                    <th>Total Score</th>
                </tr>
            </thead>
            <tbody v-for="(attempt, index) in attempts" :key="attempt.score_id">
                <tr>
                    <td>{{ index + 1 }}</td>
                    <td>{{ attempt.chapter_name }}</td>
                    <td>{{ attempt.submitted_at }}</td>
                    <td>{{ attempt.time_taken }}</td>
                    <td>{{ attempt.total_scored }}/{{ attempt.question_count }}</td>
                </tr>
            </tbody>
        </table>
        <router-link :to="{path: `/user/${route.params.user_id}/`}" class="btn btn-outline-warning text-center mb-5 mt-3 col-6 offset-3">Back to Dashboard</router-link>
    </div>
</template>





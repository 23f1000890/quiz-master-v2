<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const score = route.query.score;
</script>

<template>
  <div class="container form-body text-center mt-5 row-gap-3">
    <h3 class="text-success"> Congrats! Your Quiz Completed!</h3>
    <p class="text-light fs-5">Score: {{ score }}</p>
    <router-link :to="{
      path: `/user/${route.params.user_id}/summary/`,
    }" class="btn btn-outline-info">Evaluate your score</router-link>
    <router-link :to="{path: `/user/${route.params.user_id}/`}" class="btn btn-outline-warning ms-3">Back to Dashboard</router-link>
  </div>
</template>


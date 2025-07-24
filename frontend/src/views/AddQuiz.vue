<script setup>
import {ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const error = ref("");
const chapter_id = ref("");
const start_time = ref("");
const time_duration = ref("");
const remarks = ref("");
const message = ref([]);

// Fetch chapters for Dropdown
const fetchdata = async() => {
  try {
    const response = await fetch('http://127.0.0.1:4001/admin/', {
      method: 'GET',
      headers: {
        'content-type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    const fetchMsg = await response.json();
    // Flatten chapters from nested subjects
    message.value.chapters = (fetchMsg.subjects || []).flatMap(subject => subject.chapters || []);
  } catch (err) {
    error.value = err.message
  }
}

// Submit quiz at the backend
const handleSubmit = async() => {
  try {
    const response = await fetch("http://127.0.0.1:4001/admin/add_quiz/", {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        chapter_id: chapter_id.value,
        start_time: start_time.value.replace('T', ' '),
        time_duration: time_duration.value,
        remarks: remarks.value,
      })
    })
    const res = await response.json();
    
    if (!response.ok) {
      error.value = res.msg || 'Something went wrong!';
    } else {
      router.push({
        path: '/admin/quiz_dash/',
        query: { flash: res.msg || 'Quiz added successfully.' }
      });
    }
  } catch(err) {
    error.value = err.message
  }
}
fetchdata();
</script>


<template>
  <div class="container mt-5 form-body row-gap-3 col-6 offset-3">
    <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
    <h1 class="text-light border-3 border-bottom border-danger-subtle mb-4 mt-3 text-center">New Quiz</h1>
    <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
      {{ error }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3 col-12">
        <label for="chapter_id" class="form-label">Select Chapter:</label>
        <select type="text" v-model="chapter_id" name="chapter_id" id="chapter_id" class="form-control" required>
          <option disabled value="">-- Select Chapter --</option>
          <option v-for="chapter in message.chapters" :key="chapter.chapter_id" :value="chapter.chapter_id">
            {{ chapter.chapter_name }} ({{ chapter.chapter_id }})
          </option>
        </select>
      </div>
      <div class="mb-3 col-12">
        <label for="start_time" class="form-label">Quiz Start Date & Time:</label>
        <input type="datetime-local" v-model="start_time" name="start_time" id="start_time" class="form-control" required>
      </div>
      <div class="mb-3 col-12">
        <label for="time_duration" class="form-label">Duration (HH:MM):</label>
        <input type="text" v-model="time_duration" name="time_duration" id="time_duration" class="form-control" placeholder="e.g. 12:30" required>
      </div>
      <div class="mb-3 col-12">
        <label for="remarks" class="form-label">Remarks (Optional):</label>
        <textarea name="remarks" v-model="remarks" id="remarks" class="form-control"></textarea>
      </div>
      <button type="submit" class="btn btn-success mt-3">Add</button>&nbsp;&nbsp;
      <router-link to="/admin/quiz_dash/" class="btn btn-danger mt-3">Cancel</router-link>
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
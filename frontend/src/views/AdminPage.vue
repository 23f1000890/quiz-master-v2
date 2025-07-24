<script setup>
import { watch } from 'vue';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const message = ref([]);
const success = ref("");
const error = ref("");

const fetchdata = async() => {
    const res = await fetch("http://127.0.0.1:4001/admin/", {
        method: 'GET',
        headers: {
            'content-type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        }
    })
    message.value = await res.json();
}

const SubjectDelete = async(subject_id) => {
  try {
    const res = await fetch(`http://127.0.0.1:4001/admin/delete_subject/${subject_id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      }
    })
    const delMsg = await res.json();
    if(!res.ok) {
      error.value = delMsg.msg || "delete failed, try again!";
    } else {
      // Remove subject from the list
      message.value.subjects = message.value.subjects.filter(subject => subject.subject_id !== subject_id);

      // Show flash message without page reload
      error.value = delMsg.msg || "Subject Deleted Successfully!";
    }
  } catch(err) {
    error.value = err.message;
  }
}

const ChapterDelete = async(chapter_id) => {
  try {
    const res = await fetch(`http://127.0.0.1:4001/admin/delete_chapter/${chapter_id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      }
    })
    const delCMsg = await res.json();
    if(!res.ok) {
      error.value = delCMsg.msg || "delete failed, try again!";
    } else {
      // Remove chapter from the list
      message.value.subjects.forEach(subject =>{
        subject.chapters = subject.chapters.filter(chapter => chapter.chapter_id !== chapter_id);
      })

      // Show flash message without page reload
      error.value = delCMsg.msg || "Chapter Deleted Successfully!";
    }
  } catch(err) {
    error.value = err.message;
  }
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
    <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
      {{ error }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="d-grid d-lg-flex justify-content-lg-end mt-5 gap-2 me-5">
      <router-link to="/user_details" class="btn btn-primary"><strong>User Details</strong></router-link>
    </div>
    <div class="container form-body row-gap-3">
      <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
      <h3 class="text-light border-3 border-bottom border-danger-subtle mb-3 mt-5 pb-3">Welcome to Admin Dashboard</h3>
      <div class="d-grid d-lg-flex justify-content-lg-end mt-5 gap-2 me-5">
        <router-link to="/admin/quiz_dash" class="btn btn-primary"><strong>Quiz Portal</strong></router-link>
      </div>
      <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">Chapter-wise Subject Panel</h1>
      <div class="d-flex flex-wrap gap-3 justify-content-around">
        <div class="card" v-for="subject in message.subjects" :key="subject.subject_id">
          <div class="card-header text-center">
            <strong><em>{{ subject.subject_name }}</em></strong> <!--it fetch 'subject_name' json key; not value-->
          </div>
          <div class="card-body" >
            <table class="table table-striped mb-3 table-bordered" >
              <thead>
                <tr class="table-primary">
                  <th>Chapter Name</th>
                  <th>No of questions</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody v-for="chapter in subject.chapters" :key="chapter.chapter_id">
                <tr>
                  <td>{{ chapter.chapter_name }}</td>
                  <td>{{ chapter.question_count }}</td>
                  <td>
                    <router-link :to="{
                      path: `/edit_chapter/${chapter.chapter_id}`,
                      query: {
                        chapter_name: chapter.chapter_name,
                        description: chapter.description,
                      }
                    }" class="btn btn-warning">Edit Chapter</router-link>
                    <br>
                    <button @click="ChapterDelete(chapter.chapter_id)" class="btn btn-danger">Delete Chapter</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <router-link :to="{path: `/add_chapter/${subject.subject_id}`}" class="btn btn-success mb-3 mt-3 ms-3">+ Chapter</router-link>
            <router-link :to="{
              path: `/edit_subject/${subject.subject_id}`,
              query: {
                subject_name: subject.subject_name,
                description: subject.description,
              }
            }" class="btn btn-warning ms-2">Edit Subject</router-link>
            <button @click="SubjectDelete(subject.subject_id)" class="btn btn-danger ms-2">Delete Subject</button>
          </div>
        </div>
      </div>
      <router-link to="/add_subject" class="btn btn-success text-center mb-5 mt-3 col-6 offset-3">+ Add Subject</router-link>
    </div>
    
    
</template>

<style scoped>
.card-header {
  background-color: #de467b;
  color: #141005;
}
</style>
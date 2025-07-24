<script setup>
import { watch } from 'vue';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const message = ref([]);
const success = ref("");
const error = ref("");

const fetchdata = async() => {
  const res = await fetch("http://127.0.0.1:4001/admin/quiz_dash/", {
    method: 'GET',
    headers: {
      'content-type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    }
  })
  message.value = await res.json();
}

const QuizDelete = async(quiz_id) => {
  try {
    const res = await fetch(`http://127.0.0.1:4001/admin/delete_quiz/${quiz_id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      }
    })
    const delMsg = await res.json();
    if(!res.ok) {
      error.value = delMsg.msg || "delete failed, try again!";
    } else {
      // Remove quiz from the list
      message.value.quizzes = message.value.quizzes.filter(quiz => quiz.quiz_id !== quiz_id);

      // Show flash message without page reload
      error.value = delMsg.msg || "Quiz Deleted Successfully!";
    }
  } catch(err) {
    error.value = err.message;
  }
}

const questionDelete = async(question_id) => {
  try {
    const res = await fetch(`http://127.0.0.1:4001/admin/delete_question/${question_id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      }
    })
    const delQMsg = await res.json();
    if(!res.ok) {
      error.value = delQMsg.msg || "delete failed, try again!";
    } else {
      // Remove question from the list
      message.value.quizzes.forEach(quiz => {
        quiz.questions = quiz.questions.filter(question => question.question_id !== question_id);
      });

      // Show flash message without page reload
      error.value = delQMsg.msg || "Question Deleted Successfully!";
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
      <router-link to="/admin" class="btn btn-primary"><strong>Admin Portal</strong></router-link>
      <h3 class="text-light border-3 border-bottom border-danger-subtle mb-3 mt-5 pb-3">Welcome to Quiz Dashboard</h3>
      <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">Quiz Panel</h1>
      <div class="d-flex flex-wrap gap-3 justify-content-around">
        <div class="card" v-for="quiz in message.quizzes" :key="quiz.quiz_id">
          <div class="card-header text-center">
            <strong><u>Q_ID</u></strong>
            <br>
            <strong><em><u>{{ quiz.quiz_id }}</u></em></strong>
            <br>
            <strong class="text-light">Chapter: {{ quiz.chapter_name }}</strong>
          </div>
          <div class="card-subtitile text-center text-secondary border-warning border-3 border-bottom">
            <strong><em>--Subject: {{quiz.subject_name}}--</em></strong>
          </div>
          <div class="card-body">
            <table class="table table-striped mb-3 table-bordered" >
              <thead>
                <tr class="table-primary">
                  <th>Question ID</th>
                  <th>Q_Title</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody v-for="question in quiz.questions" :key="question.question_id">
                <tr>
                  <td>{{ question.question_id }}</td>
                  <td>{{ question.question_title }}</td>
                  <td>
                    <router-link :to="{
                      path: `/admin/edit_question/${question.question_id}/`,
                      query: {
                        chapter_id: quiz.chapter_id,
                        chapter_name: quiz.chapter_name,
                        question_title: question.question_title,
                        question_statement: question.question_statement,
                        option1: question.option1,
                        option2: question.option2,
                        option3: question.option3,
                        option4: question.option4,
                        correct_answer: question.correct_answer,
                      }
                    }" class="btn btn-warning">Edit Question</router-link>
                    <br>
                    <button @click="questionDelete(question.question_id)" class="btn btn-danger">Delete Question</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <router-link :to="{
              path: `/admin/add_question/${quiz.quiz_id}/`,
              query: {
                chapter_id: quiz.chapter_id,
                chapter_name: quiz.chapter_name,
              },
            }" class="btn btn-success mb-3 mt-3 ms-3">+ Question</router-link>
            <router-link :to="{
              path: `/admin/edit_quiz/${quiz.quiz_id}/`,
              query: {
                chapter_id: quiz.chapter_id,
                start_time: quiz.start_time,
                time_duration: quiz.time_duration,
                remarks: quiz.remarks,
              },
            }" class="btn btn-warning ms-2">Edit Quiz</router-link>
            <button @click="QuizDelete(quiz.quiz_id)" class="btn btn-danger ms-2">Delete Quiz</button>
          </div>
        </div>
      </div>
      <router-link to="/admin/add_quiz/" class="btn btn-success text-center mb-5 mt-3 col-6 offset-3">+ New Quiz</router-link>
    </div>
    
    
</template>

<style scoped>
.card-header {
  background-color: #de467b;
  color: #141005;
}
</style>
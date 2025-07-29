<script setup>
import { ref } from 'vue';
import { useRoute, useRouter} from 'vue-router';

const route = useRoute();
const router = useRouter();

const user_id = route.params.user_id;
const quiz_id = route.params.quiz_id;
const chapter_name = ref(route.query.chapter_name || "");
const message = ref([]);
const showConfirm = ref(false);
const selectedAnswers = ref([]);
const startTime = ref(null);
const endTime = ref(null);
const timeLeft = ref(0);
const timerInterval = ref(null);

const quizData = async() => {
  const response = await fetch(`http://127.0.0.1:4001/user/${user_id}/quiz/${quiz_id}/start/`, {
    headers: {
        'content-type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
  });

  message.value = await response.json();

  // Parse start_time and time_duration from server response
  const start = new Date(message.value.start_time);
  const [minutes, seconds] = message.value.time_duration.split(":").map(Number);
  const durationMs = (minutes * 60 + seconds) * 1000;

  startTime.value = start;
  endTime.value = new Date(start.getTime() + durationMs);

  updateTimer(); // Start countdown
  timerInterval.value = setInterval(updateTimer, 1000);

}

const updateTimer = () => {
  const now = new Date();
  const remaining = Math.max(0, endTime.value - now);
  timeLeft.value = Math.floor(remaining / 1000);

  if (remaining <= 0) {
    clearInterval(timerInterval.value);
    confirmSubmission(); // auto-submit when time expires
  }
};

const formatTime = (seconds) => {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
};

const handleSubmit = () => {
  showConfirm.value = true;
}

const cancelSubmission = () => {
  showConfirm.value = false;
}

const confirmSubmission = async() => {
  const formattedAnswers = Object.entries(selectedAnswers.value).map(
    ([question_id, selected_answer]) => ({
      question_id,
      selected_answer,
    })
  )
  const response = await fetch(`http://127.0.0.1:4001/user/${user_id}/quiz/${quiz_id}/submit/`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
    body: JSON.stringify({
      answers: formattedAnswers,
    })
  })

  const res = await response.json();
  if(!response.ok) {
    alert("Error Submitting Quiz!!!")
  } else {
    router.push({
      path: `/user/${user_id}/quiz/${quiz_id}/submit/`,
      query: {
        score: res.total_scored,
      }
    })
  }
}
quizData();
</script>

<template>
    
    <div class="container form-body row-gap-3 mt-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <h1 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">-- Quiz - {{ quiz_id }} --</h1>
        <h3 class="text-info border-primary border-bottom border-2 pb-3 mb-3 mt-5" align="center">-- Chapter Name - {{ chapter_name }} --</h3>
        <h4 class="text-danger text-center">Time Remaining: {{ formatTime(timeLeft) }}</h4>
        <div class="card card-body mb-5" v-for="(question,index) in message.questions" :key="question.question_id">
            <span class="text-light header">Q{{ index+1 }}: {{ question.question_title }}</span>
            <span class="mb-3 text-light statement">{{ question.question_statement }}</span>
            <div class="form-check" v-for="(option, index) in question.options" :key="index">
                <input type="radio" v-model="selectedAnswers[question.question_id]" class="form-check-input" :name="'question_'+question.question_id" :value="option" :id="`q${question.question_id}_opt${index}`">
                <label class="form-check-label text-light" :for="`q${question.question_id}_opt${index}`">
                    {{ option }}
                </label>
            </div>
        </div>
        <div class="card" v-if="showConfirm">
          <h3 class="text-light card-header">Do you really want to Submit?</h3>
          <button class="btn btn-success" @click="confirmSubmission">OK</button>
          <button class="btn btn-secondary" @click="cancelSubmission ">No, Return to Quiz</button>
        </div>
        <button :disabled="timeLeft <= 0" @click="handleSubmit" class="btn btn-warning text-center mb-5 mt-3 col-6 offset-3">Submit Quiz</button>
    </div>

</template>

<style scoped>
.card {
    background-color: #141005;
    border-color: greenyellow;
}
.header,.statement {
    font-size: 2rem;
}

</style>
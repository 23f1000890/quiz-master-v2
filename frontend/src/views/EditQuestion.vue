<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// const quiz_id = route.params.quiz_id;
const question_id = route.params.question_id;
const chapter_id = ref(route.query.chapter_id || "");
const chapter_name = ref(route.query.chapter_name || "");
const question_title = ref(route.query.question_title || "");
const question_statement = ref(route.query.question_statement || "");
const error = ref("");

const correct_answer = ref(route.query.correct_answer || "");
const options = ref([route.query.option1 || "", route.query.option2 || "", route.query.option3 || "", route.query.option4 || ""]);

const handleSubmit = async() => {
    try{
        const response = await fetch(`http://127.0.0.1:4001/admin/edit_question/${question_id}/`,{
            method: 'PUT',
            headers: {
                'content-type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify({
                question_title: question_title.value,
                question_statement: question_statement.value,
                option1: options.value[0],
                option2: options.value[1],
                option3: options.value[2],
                option4: options.value[3],
                correct_answer: correct_answer.value,
            }),
        })

        const res = await response.json();
        if(!response.ok) {
            error.value = res.msg || "Something went wrong!";
        } else {
            router.push({
                path: '/admin/quiz_dash',
                query: { flash: res.msg || 'Question Updated Successfully'}
            })
        }
    } catch(err){
        error.value = err.message;
    }
}

</script>

<template>
    <div class="container mt-5 form-body row-gap-3 col-6 offset-3">
        <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
        <h1 class="text-light border-3 border-bottom border-danger-subtle mb-4 mt-3 text-center">Update your Question</h1>
        <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
            {{ error }}
            <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <form @submit.prevent="handleSubmit">
            <div class="mb-3 col-12">
                <label for="chapter_id" class="form-label">Chapter ID:</label>
                <input type="text" v-model="chapter_id" name="chapter_id" id="chapter_id" class="form-control" readonly>
            </div>
            <div class="mb-3 col-12">
                <label for="chapter_name" class="form-label">Chapter Name:</label>
                <input type="text" v-model="chapter_name" name="chapter_name" id="chapter_name" class="form-control" readonly>
            </div>
            <div class="mb-3 col-12">
                <label for="question_title" class="form-label">Question Title:</label>
                <input type="text" v-model="question_title" name="question_title" id="question_title" class="form-control" placeholder="Enter the Question title" required>
            </div>
            <div class="mb-3 col-12">
                <label for="question_statement" class="form-label">Question Statement:</label>
                <textarea name="question_statement" v-model="question_statement" id="question_statement" class="form-control" required></textarea>
            </div>
            <div class="mb-3 col-12">
                <h3 class="mb-3 text-center form-label">Single Option Correct</h3>
                <div class="mb-3 col-12">
                    <label class="form-label">Options:</label>
                    <input type="text" v-model="options[0]" class="form-control mb-3" name="option1" placeholder="Option 1:" required>
                    <input type="text" v-model="options[1]" class="form-control mb-3" name="option2" placeholder="Option 2:" required>
                    <input type="text" v-model="options[2]" class="form-control mb-3" name="option3" placeholder="Option 3:" required>
                    <input type="text" v-model="options[3]" class="form-control mb-3" name="option4" placeholder="Option 4:" required>
                </div>
                <div class="mb-3 col-12">
                    <label for="correct_answer" class="form-label">Correct Answer:</label>
                    <select v-model="correct_answer" name="correct_answer" class="form-control" id="correct_answer" required>
                        <option disabled selected value="">Select Correct Answer</option>
                        <option value="1">Option 1</option>
                        <option value="2">Option 2</option>
                        <option value="3">Option 3</option>
                        <option value="4">Option 4</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="btn btn-success mt-3 mb-5">Update</button>
            <router-link to="/admin/quiz_dash" class="btn btn-danger mt-3 ms-3 mb-5">Cancel</router-link>
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
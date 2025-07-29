<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isLogin = ref(true);
const email = ref("");
const password = ref("");
const username = ref("");
const full_name = ref("");
const dob = ref("");
const qualification = ref("");
const location = ref("");
const error = ref("");
const success = ref("");

const handleLogin = async() => {
  try {
    const response = await fetch("http://127.0.0.1:4001/auth/login/", {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        email: email.value, 
        password: password.value,
      }),
    })

    const message = await response.json();
    if(!response.ok) {
      error.value = message.msg || "Invalid login, failed!!!";
    } else {
      router.push({
        path: message.role === "admin" ? "/admin/" : `/user/${message.user_id}/`,
        query: { flash: message.msg || message.role === "admin" ? "Welcome to Admin Portal" : "Welcome to User Portal"}
      })
    }

    localStorage.setItem("access_token", message.access_token);
    localStorage.setItem("refresh_token", message.refresh_token);
    localStorage.setItem("role", message.role);
  
  } catch (err) {
    error.value = err.message; 
  }
}

const handleRegister = async() => {
  try {
    const response = await fetch("http://127.0.0.1:4001/auth/register/", {
      method: 'POST',
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        username: username.value,
        full_name: full_name.value,
        qualification: qualification.value,
        dob: dob.value,
        location: location.value,
      }),
    })
    const message = await response.json();
    if(!response.ok) {
      error.value = message.msg || "Registration Denied!!!"
    } else {
      router.push({
        path: '/login',
        query: { flash: message.msg || "Registration successfull"}
      })
    };

    isLogin.value = true;
  } catch (err) {
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
</script>


<template>
  <div class="container mt-5 form-body row-gap-3 col-6 offset-3">
    <h1 class="text-success" align="center">Welcome to intelliquest 2.0</h1>
    <h1 class="text-light border-3 border-bottom border-danger-subtle mb-4 mt-3 text-center">{{ isLogin ? "login" : "Register" }}</h1>
    <div class="alert alert-danger alert-dismissible fade show col-4 offset-8 mt-3" v-if="error" role="alert">
      {{ error }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div class="alert alert-success alert-dismissible fade show col-4 offset-8 mt-3" v-if="success" role="alert">
      {{ success }}
      <button type="button" class="btn-close btn-light" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
      <div class="mb-3 col-12">
        <label for="email" class="form-label">Email:</label>
        <input type="email" v-model="email" name="email" id="email" class="form-control" placeholder="Enter your Email" required>
      </div>
      <div class="mb-3 col-12">
        <label for="password" class="form-label">Password:</label>
        <input type="password" v-model="password" name="password" id="password" class="form-control" placeholder="Enter your Password" required>
      </div>
      <div class="mb-3 col-12" v-if="!isLogin">
        <label for="username" class="form-label">Username:</label>
        <input type="text" v-model="username" name="username" id="username" class="form-control" placeholder="Enter your Username" required>
      </div>
      <div class="mb-3 col-12" v-if="!isLogin">
        <label for="full_name" class="form-label">Full Name:</label>
        <input type="text" v-model="full_name" name="full_name" id="full_name" class="form-control" placeholder="Enter your Full Name" required>
      </div>
      <div class="mb-3 col-12" v-if="!isLogin">
        <label for="dob" class="form-label">Date of Birth:</label>
        <input type="date" v-model="dob" name="dob" id="dob" class="form-control">
      </div>
      <div class="mb-3 col-12" v-if="!isLogin">
        <label for="qualification" class="form-label">Your Qualification:</label>
        <input type="text" v-model="qualification" name="qualification" id="qualification" class="form-control" placeholder="Enter your Qualifications">
      </div>
      <div class="mb-3 col-12" v-if="!isLogin">
        <label for="location" class="form-label">Your Location:</label>
        <input type="text" v-model="location" name="location" id="location" class="form-control" placeholder="Enter your location">
      </div>
      <button type="submit" class="btn btn-success mt-3 offset-3 col-6">{{ isLogin ? "login" : "Register" }}</button>
    </form>
    <button type="button" @click="isLogin = !isLogin" class="btn btn-link mt-3 col-6 offset-3">
      {{ isLogin ? "Need to Register" : "Already have an account" }}
    </button>
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
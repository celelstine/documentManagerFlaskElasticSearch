<template>
  <div class="col-sm-4 col-sm-offset-4">
    <h2>Create an account</h2>
    <div class="alert alert-danger" v-if="error">
      <p>{{ error }}</p>
    </div>
    <form @submit.prevent="signupuser()">
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          placeholder="Enter your email"
          v-model="credentials.email"
        >
      </div>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          placeholder="Enter your full name"
          v-model="credentials.name"
        >
      </div>
      <div class="form-group">
        <input
          type="password"
          class="form-control"
          placeholder="Enter your password"
          v-model="credentials.password"
        >
      </div>
      <button class="btn btn-primary" type="submit">Sign Up</button>
    </form>
  </div>
</template>


<script>
import axios from "axios";
export default {
  data() {
    return {
      credentials: {
        email: "",
        password: "",
        name: ""
      },
      error: ""
    };
  },
  methods: {
    signupuser() {
      const payload = {
        email: this.credentials.email,
        password: this.credentials.password,
        name: this.credentials.name
      };
      const path = `http://localhost:5000/api/signup`;
      axios
        .post(path, payload)
        .then(response => {
          localStorage.setItem('token', response.data.jwt)

          // Redirect to the dashboard page.
         this.$router.push('home') 
        })
        .catch(error => {
          this.error = error.response.data.message;
        });
    }
  }
};
</script>

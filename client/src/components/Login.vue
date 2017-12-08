<template>
    <div class="col-sm-4 col-sm-offset-4">
      <h2>Log In</h2>
      <div class="alert alert-danger" v-if="error">
        <p>{{ error }}</p>
      </div>
      <form @submit.prevent="loginuser()">
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
            type="password"
            class="form-control"
            placeholder="Enter your password"
            v-model="credentials.password"
          >
        </div>
        <router-link to="/signup">Don't have an account? Sign up here</router-link>
        <div>
          <button class="btn btn-primary" type="submit">Log in</button>          
        </div>
      </form>
    </div>
  </template>

<script>
import axios from 'axios'
import router from 'vue'
export default {
  data () {
    return {
      credentials: {
          email: '',
          password: ''
        },
      error: ''
    }
  },
  methods: {
    loginuser () {
      const payload = {
        email: this.credentials.email,
        password: this.credentials.password
      }
      const path = `http://localhost:5000/api/login/`
      axios.post(path, payload)
      .then(response => {
        localStorage.setItem('token', response.data.jwt)
       
        // Redirect to the dashboard page.
        this.$router.push('home') 
      })
      .catch(error => {
        this.error = error.response.data.message
      })
    }
  }
}
</script>

<template>
  <div>
    <NavBar/>
    <div>
      <form class="form-signin" @submit.prevent="loginuser()">       
        <h2 class="form-signin-heading">New Doc</h2>
        <input type="text" class="form-control" name="username" placeholder="title" v-model="credentials.title" required="" autofocus="" />
        <br>
        <div class="form-group">
          <label for="sel1">Select accessright</label>
          <select class="form-control" v-model="credentials.accessRight" id="sel1">
            <option>Public</option>
            <option>Private</option>
            <option>Role</option>
          </select>
        </div>
        <br>
        <div class="form-group">
          <textarea class="form-control" rows="5" id="comment" placeholder="body" v-model="credentials.body"></textarea>
        </div>      
        <button class="btn btn-lg btn-primary btn-block" type="submit">Create document</button>   
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import NavBar from './NavBar'
export default {
  data () {
    return {
      credentials: {
        title: '',
        body: '',
        accessRight: 'Public'
      }
    }
  },
  components: {
    'NavBar': NavBar
  },
  methods: {
    loginuser () {
      const payload = {
        title: this.credentials.title,
        body: this.credentials.body,
        accessRight: this.credentials.accessRight
      }
      axios.defaults.headers.common['Authorization'] = localStorage.token;
      const path = `http://localhost:5000/api/documents`
      axios.post(path, payload)
      .then(response => {
        this.$router.push('home') 
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<template>
  <div>
    <NavBar/>
    <div class="container">
      <form @submit.prevent="search()">
        <div class="col-lg-6">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="Search for..." v-model="searchTerm">
            <span class="input-group-btn">
              <button class="btn btn-secondary" type="submit">Go!</button>
            </span>
          </div>
        </div>
      </form>      
    </div>
    <div class="row" v-for="document in documents">
      <div class="col-sm-6">
        <div class="card">
          <div class="card-block">
            <h3 class="card-title">{{ document.document.title }}</h3>
            <p class="card-text">{{ document.document.body }}</p>
            <p class="card-link">Created by: {{document.document.owner}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>  
</template>

<script>
  import axios from 'axios';
  import NavBar from './NavBar'
  export default {
    data() {
      return {
        searchTerm: '',
        documents: []
      }
    },
    components: {
      'NavBar': NavBar
    },
    methods: {
      search() {
        const searchTerm = this.searchTerm
        axios.defaults.headers.common['Authorization'] = localStorage.token;
        const path = `http://localhost:5000/api/search/${searchTerm}`
        axios.get(path)
        .then(response => {
          this.documents = response.data.documents
        })
        .catch(error => {
          console.log(error)
        })  
      }
    }
  }
</script>

import Vue from 'vue';
// import axios from 'axios';
import App from './App';
import router from './router';

Vue.config.productionTip = false;

// const setAuthorizationHeader = (token) => {
//   if (token) {
//     axios.defaults.headers.common.Authorization = token;
//     console.log('token here mehn', axios.defaults.headers.common['Authorization']);
//     console.log('token here mehn2', axios.defaults);
//   } else {
//     delete axios.defaults.headers.common['Authorization'];
//   }
// };

// if (localStorage.token) {
//   setAuthorizationHeader(localStorage.token);
// }


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
});

import Vue from 'vue';
import Router from 'vue-router';

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/dashboard', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/login', component: 'Login' },
  { path: '/signup', component: 'Signup' },
  { path: '/new-doc', component: 'Document' },
  { path: '/home', component: 'Dashboard' },
  { path: '/search', component: 'SearchDocs' },
  { path: '*', component: 'NotFound' },
];
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`),
  };
});
Vue.use(Router);
export default new Router({
  routes,
  mode: 'history',
});

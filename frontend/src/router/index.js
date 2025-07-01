import { createRouter, createWebHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import Login from '../pages/Login.vue'
import SearchResults from '../pages/SearchResults.vue'
import HotelDetail from '../pages/HotelDetail.vue'
import MapResults from '../pages/MapResults.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/map',
    name: 'Map',
    component: MapResults
  },
  
  {
    path: '/hotel/:id', 
    name: 'HotelDetail',
    component: HotelDetail,
    props: true 
  }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

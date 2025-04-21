import { createRouter, createWebHistory } from 'vue-router';
import Chat from '../components/Chat.vue';

const routes = [
  { path: '/chat', component: Chat },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

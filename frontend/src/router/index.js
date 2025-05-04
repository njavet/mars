import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue'
import About from '../components/About.vue'
import Chatbot from '../components/Chatbot.vue'
import Assistant from '../components/Assistant.vue'
import Evaluation from '../components/Evaluation.vue'

const routes = [
  { path: '/', name: 'home', component: Home},
  { path: '/about', name: 'about', component: About},
  { path: '/chatbot', name: 'chatbot', component: Chatbot, props: true },
  { path: '/assistant', name: 'assistant', component: Assistant, props: true },
  { path: '/evaluation', name: 'evaluation', component: Evaluation, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

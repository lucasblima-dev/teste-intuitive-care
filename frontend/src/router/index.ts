import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '@/views/DashboardView.vue';
import ListaOperadores from '@/views/ListaOperadores.vue';
import DetalhesIOperador from '@/views/DetalhesIOperador.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/operadoras',
      name: 'operadoras',
      component: ListaOperadores
    },
    {
      path: '/operadoras/:id',
      name: 'detalhes',
      component: DetalhesIOperador
    }
  ]
});

export default router;
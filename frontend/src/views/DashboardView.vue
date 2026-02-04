<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, type ChartData } from 'chart.js';
import api from '../services/api';
import type { StatsUF } from '../types';
import AppCard from '../components/ui/AppCard.vue';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const chartData = ref<ChartData<'bar'>>({ labels: [], datasets: [] });
const loaded = ref(false);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#10b981',
      bodyColor: '#fff',
      borderColor: '#334155',
      borderWidth: 1,
      padding: 10,
    }
  },
  scales: {
    y: {
      grid: { color: '#334155', tickColor: '#334155' },
      ticks: { color: '#94a3b8' }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94a3b8' }
    }
  }
};

const fetchStats = async () => {
  try {
    const { data } = await api.get<StatsUF[]>('/estatisticas');
    
    chartData.value = {
      labels: data.map(d => d.uf),
      datasets: [{
        label: 'Total de Despesas',
        backgroundColor: '#10b981',
        borderRadius: 4,
        hoverBackgroundColor: '#34d399',
        data: data.map(d => d.total_despesas)
      }]
    };
    loaded.value = true;
  } catch (error) {
    console.error("Erro ao carregar gráfico", error);
  }
};

onMounted(fetchStats);
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <header>
      <h1 class="text-2xl font-bold text-white">Painel de Controle</h1>
      <p class="text-muted">Visão geral das despesas hospitalares por estado.</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <AppCard class="lg:col-span-2 h-100">
        <h2 class="text-lg font-semibold mb-4 text-white">Despesas por UF</h2>
        <div class="h-75" v-if="loaded">
          <Bar :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="h-full flex items-center justify-center text-muted">
          Carregando dados...
        </div>
      </AppCard>

      <AppCard>
        <h2 class="text-lg font-semibold mb-4 text-white">Status do Sistema</h2>
        <div class="space-y-4">
          <div class="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg">
            <span class="text-muted text-sm">Status da API</span>
            <span class="text-emerald-400 text-sm font-bold flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Online
            </span>
          </div>
          </div>
      </AppCard>
    </div>
  </div>
</template>
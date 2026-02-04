<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import type { Operadora, Despesa } from '../types';
import AppCard from '..//components/ui/AppCard.vue';
import AppButton from '..//components/ui/AppButton.vue';

const route = useRoute();
const router = useRouter();
const operadora = ref<Operadora | null>(null);
const despesas = ref<Despesa[]>([]);
const loading = ref(true);

const formatCurrency = (val: number) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
};

const fetchData = async () => {
  const id = route.params.id;
  try {
    const resDespesas = await api.get(`/operadoras/${id}/despesas`);
    despesas.value = resDespesas.data;

    const resOperadora = await api.get(`/operadoras?search=${id}`);
  
    if (resOperadora.data.data && resOperadora.data.data.length > 0) {
      operadora.value = resOperadora.data.data[0];
    }
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="space-y-6">
    <AppButton variant="outline" @click="router.back()">
      &larr; Voltar
    </AppButton>

    <div v-if="loading" class="text-center text-muted py-10">Carregando informações...</div>

    <template v-else>
      <div class="bg-linear-to-r from-emerald-900/50 to-slate-900 border border-emerald-500/30 rounded-xl p-8 shadow-lg">
        <h2 class="text-sm text-emerald-400 font-mono mb-2">REGISTRO ANS: {{ route.params.id }}</h2>
        <h1 class="text-3xl font-bold text-white mb-2">
          {{ operadora?.razao_social || 'Razão Social Indisponível' }}
        </h1>
        <div class="flex gap-4 text-sm text-slate-300">
          <span class="flex items-center gap-1">
            <i class="w-2 h-2 bg-emerald-500 rounded-full"></i> Ativo
          </span>
        </div>
      </div>

      <h3 class="text-xl font-bold text-white mt-8">Histórico de Eventos</h3>
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <AppCard v-for="(despesa, index) in despesas" :key="index" class="border-l-4 border-l-emerald-500">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs bg-slate-700 text-white px-2 py-1 rounded">
              {{ despesa.trimestre }} / {{ despesa.ano }}
            </span>
          </div>
          <p class="text-slate-300 text-sm mb-4 min-h-[40px]">{{ despesa.descricao_conta }}</p>
          <div class="text-2xl font-bold text-white">
            {{ formatCurrency(despesa.valor) }}
          </div>
        </AppCard>
      </div>
      
      <div v-if="despesas.length === 0" class="text-center text-muted py-10 bg-surface rounded-xl">
        Nenhuma despesa registrada para este período.
      </div>
    </template>
  </div>
</template>
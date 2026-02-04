<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import type { Operadora, PaginationMeta } from '../types';
import AppCard from '../components/ui/AppCard.vue';
import AppInput from '../components/ui/AppInput.vue';
import AppButton from '../components/ui/AppButton.vue';

const router = useRouter();
const operadoras = ref<Operadora[]>([]);
const search = ref('');
const meta = ref<PaginationMeta>({ page: 1, limit: 10, total: 0 });
const loading = ref(false);
let debounceTimeout: number;

const fetchOperadoras = async () => {
  loading.value = true;
  try {
    const params = {
      search: search.value,
      page: meta.value.page,
      limit: meta.value.limit
    };
    
    const { data } = await api.get('/operadoras', { params });
    operadoras.value = data.data || data;
    meta.value.total = data.total || 100; 
  } catch (error) {
    //console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = (val: string) => {
  search.value = val;
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    meta.value.page = 1;
    fetchOperadoras();
  }, 500);
};

const changePage = (step: number) => {
  const newPage = meta.value.page + step;
  if (newPage < 1) return;
  
  // if (newPage > lastPage) return;
  
  meta.value.page = newPage;
  fetchOperadoras();
};

const goToDetails = (id: number) => {
  router.push(`/operadoras/${id}`);
};

onMounted(fetchOperadoras);
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white">Operadoras</h1>
        <p class="text-muted">Gerenciamento e monitoramento de registros ANS.</p>
      </div>
      <div class="w-full md:w-64">
        <AppInput 
          :model-value="search" 
          @update:model-value="handleSearch" 
          placeholder="Buscar operadora..." 
        />
      </div>
    </div>

    <AppCard class="overflow-hidden p-0">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-muted">
          <thead class="bg-slate-900/50 text-xs uppercase text-slate-300">
            <tr>
              <th class="px-6 py-4">Registro ANS</th>
              <th class="px-6 py-4">Razão Social</th>
              <th class="px-6 py-4">UF</th>
              <th class="px-6 py-4 text-right">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr v-if="loading" v-for="i in 5" :key="i" class="animate-pulse">
               <td colspan="4" class="px-6 py-4"><div class="h-4 bg-slate-700 rounded w-full"></div></td>
            </tr>
            
            <tr 
              v-else 
              v-for="op in operadoras" 
              :key="op.reg_ans"
              class="hover:bg-slate-700/30 transition-colors cursor-pointer"
              @click="goToDetails(op.reg_ans)"
            >
              <td class="px-6 py-4 font-mono text-emerald-400">#{{ op.reg_ans }}</td>
              <td class="px-6 py-4 font-medium text-white">
                {{ op.razao_social || 'Razão Social Não Informada' }}
              </td>
              <td class="px-6 py-4">
                <span v-if="op.uf" class="bg-slate-700 text-white px-2 py-1 rounded text-xs">{{ op.uf }}</span>
                <span v-else class="text-slate-600">-</span>
              </td>
              <td class="px-6 py-4 text-right">
                <span class="text-primary text-xs hover:underline">Ver Detalhes &rarr;</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="p-4 border-t border-slate-700 flex justify-between items-center">
        <span class="text-xs text-muted">Página {{ meta.page }}</span>
        <div class="flex gap-2">
          <AppButton variant="outline" :disabled="meta.page === 1" @click="changePage(-1)">Anterior</AppButton>
          <AppButton variant="outline" @click="changePage(1)">Próximo</AppButton>
        </div>
      </div>
    </AppCard>
  </div>
</template>
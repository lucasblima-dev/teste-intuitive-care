<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const isSidebarOpen = ref(false)

const closeSidebar = () => {
  isSidebarOpen.value = false
}
</script>

<template>
  <div class="flex h-screen bg-slate-900 text-slate-100 font-sans overflow-hidden">
    
    <div 
      v-if="isSidebarOpen" 
      @click="closeSidebar"
      class="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm transition-opacity"
    ></div>

    <aside 
      class="fixed inset-y-0 left-0 z-50 w-64 bg-slate-800 border-r border-slate-700 flex flex-col transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-6 flex items-center gap-3">
        <div class="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <span class="text-slate-900 font-bold text-xl">I</span>
        </div>
        <span class="text-xl font-bold tracking-tight text-white">Intuitive<span class="text-emerald-500">Care</span></span>
        
        <button @click="closeSidebar" class="ml-auto md:hidden text-slate-400 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-2">
        <RouterLink 
          to="/" 
          @click="closeSidebar"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition-all duration-200"
          active-class="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 shadow-sm border border-emerald-500/10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          <span class="font-medium">Dashboard</span>
        </RouterLink>

        <RouterLink 
          to="/operadoras" 
          @click="closeSidebar"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition-all duration-200"
          active-class="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 shadow-sm border border-emerald-500/10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          <span class="font-medium">Operadoras</span>
        </RouterLink>
      </nav>

      <div class="p-4 border-t border-slate-700 bg-slate-800/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center text-slate-400 border border-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          </div>
          <div>
            <p class="text-sm font-medium text-white">Admin</p>
            <p class="text-xs text-emerald-500 font-medium">Lucas Lima</p>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 flex flex-col h-screen overflow-hidden relative w-full">
      
      <header class="md:hidden bg-slate-800 border-b border-slate-700 p-4 flex items-center justify-between sticky top-0 z-30">
        <div class="flex items-center gap-2">
           <div class="w-6 h-6 bg-emerald-500 rounded flex items-center justify-center">
              <span class="text-slate-900 font-bold text-xs">I</span>
           </div>
           <span class="font-bold text-white">Intuitive Care</span>
        </div>
        <button @click="isSidebarOpen = true" class="text-slate-300 hover:text-white p-1 rounded hover:bg-slate-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      </header>

      <div class="flex-1 overflow-auto bg-slate-900 p-4 md:p-8 scroll-smooth">
        <div class="max-w-7xl mx-auto">
          <RouterView v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </RouterView>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>